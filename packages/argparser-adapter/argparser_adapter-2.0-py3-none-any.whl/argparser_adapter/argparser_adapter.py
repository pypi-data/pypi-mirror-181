#!/usr/bin/env python3
import argparse
import functools
import inspect
import itertools
from typing import Any, Dict

from . import adapter_logger

METHOD_METADATA: Dict[str, 'CommandLine'] = {}


class CommandLine(object):
    def __init__(self, required: bool = False, default=None):
        self.required = required
        self.default = default

    def __call__(self, original_func):
        @functools.wraps(original_func)
        def wrappee(*args, **kwargs):
            original_func(*args, **kwargs)

        self.client = original_func
        METHOD_METADATA[original_func.__qualname__] = self
        return wrappee

    def __str__(self):
        return f"{self.client.__qualname__} required {self.required} default {self.default}"


class ArgparserAdapter:
    BOOL_YES = ('true', 'on', 'yes')
    BOOL_NO = ('false', 'off', 'no')

    _INSTANCE: 'ArgparserAdapter' = None

    def __init__(self, client, *, prefix: str = 'do_', group: bool = True, required: bool = False,
                 explicit: bool = False):
        """client: object to analyze for methods
        prefix: name to start method withs for arguments
        group: put arguments in an arparse group
        required: if using a group, make it required"""
        if not ArgparserAdapter._INSTANCE is None:
            raise ValueError(f"Only one {self.__class__.__name__} currently supported")
        ArgparserAdapter._INSTANCE = self
        self.client = client
        self.argadapt_prefix = prefix
        self.argadapt_required = required
        self.argadapt_group = group
        self.explicit = explicit
        self._argadapt_dict = {}

    def param_conversion_exception(self, e: Exception, method_name: str, parameter_name: str, parameter_type: type,
                                   value: str) -> Any:
        """
        :param e: Exception thrown
        :param method_name: called method
        :param parameter_name: parameter name
        :param parameter_type:
        :param value: value passed on command line
        :return: valid value for parameter_type, or raise exception
        """
        raise ValueError(f"conversion error of method {method_name} parameter {parameter_name} value {value} {e}")

    def register(self, argparser: argparse.ArgumentParser) -> None:
        """Add arguments to argparser based on self.argadapt_settings"""
        use_decorator = len(METHOD_METADATA) > 0
        needarg = False
        if self.argadapt_group:
            ap = argparser.add_mutually_exclusive_group(required=self.argadapt_required)
            arequired = False
            needarg = True
        else:
            ap = argparser
            arequired = self.argadapt_required
        plen = len(self.argadapt_prefix)
        for d in inspect.getmembers(self.client, self.__only_methods):
            name, mobj = d
            kwargs = {}
            if (meta := METHOD_METADATA.get(mobj.__func__.__qualname__, None)) is not None:
                if meta.required and meta.default is not None:
                    adapter_logger.warning(f"Default with required {meta}")
                else:
                    adapter_logger.info(meta)
                kwargs = {'required': meta.required}
                if meta.default is not None:
                    kwargs['default'] = meta.default

            doc = inspect.getdoc(mobj)
            startswith = not use_decorator and name.startswith(self.argadapt_prefix)
            if startswith or meta is not None:
                needarg = False
                if startswith:
                    arg = name[plen:]
                else:
                    arg = name
                sig = inspect.signature(mobj, follow_wrapped=True)
                ptypes = [p for _, p in sig.parameters.items()]
                self._argadapt_dict[arg] = (getattr(self.client, name), ptypes)
                nargs = len(ptypes)
                if nargs > 0:
                    desc = tuple(sig.parameters.keys())
                    if meta is not None:
                        ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, help=doc, **kwargs)
                    else:
                        ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, required=arequired, help=doc)
                else:
                    if meta is not None:
                        ap.add_argument(f'--{arg}', action='store_true', help=doc, **kwargs)
                    else:
                        ap.add_argument(f'--{arg}', action='store_true', help=doc)
            if needarg:
                raise ValueError(
                    f"No methods marked @CommandLine staring with {self.argadapt_prefix} found and group is required")

    @staticmethod
    def _interpret(typ, value):
        if typ.annotation != bool:
            return typ.annotation(value)
        lvalue = value.lower()
        if lvalue in ArgparserAdapter.BOOL_YES:
            return True
        if lvalue in ArgparserAdapter.BOOL_NO:
            return False
        try:
            return bool(int(value))
        except:
            pass
        vals = itertools.chain(ArgparserAdapter.BOOL_YES, ArgparserAdapter.BOOL_NO)
        raise ValueError(f"Unable to interpret {value} as bool. Pass one of {','.join(vals)} or integer value")

    def call_specified_methods(self, args: argparse.Namespace) -> None:
        """Call method from parsed args previously registered"""
        for name, mspec in self._argadapt_dict.items():
            params = getattr(args, name, None)
            if params:
                method, iparams = mspec
                if params is True:  # noaction store_true argument
                    method()
                    continue
                if not isinstance(params, list):
                    params = [params]
                #                assert (len(params) == len(iparams))
                callparams = []
                for value, ptype in zip(params, iparams):
                    if ptype.annotation != ptype.empty:
                        try:
                            value = self._interpret(ptype, value)
                        except Exception as e:
                            value = self.param_conversion_exception(e, name, ptype.name, ptype.annotation, value)
                    callparams.append(value)
                method(*callparams)

    @staticmethod
    def __only_methods(x):
        return inspect.ismethod(x)
