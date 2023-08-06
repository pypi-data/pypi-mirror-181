#!/usr/bin/env python3
import argparse
import inspect
import itertools
from typing import Any


class ArgparserAdapter:

    BOOL_YES = ('true', 'on', 'yes')
    BOOL_NO = ('false', 'off', 'no')

    def __init__(self, client, *, prefix='do_', group=True, required=False):
        """client: object to analyze for methods
        prefix: name to start method withs for arguments
        group: put arguments in an arparse group
        required: if using a group, make it required"""
        self.client = client
        self.argadapt_prefix = prefix
        self.argadapt_required = required
        self.argadapt_group = group
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
            doc = inspect.getdoc(mobj)
            if name.startswith(self.argadapt_prefix):
                needarg = False
                arg = name[plen:]
                sig = inspect.signature(mobj)
                ptypes = [p for _, p in sig.parameters.items()]
                self._argadapt_dict[arg] = (getattr(self.client, name), ptypes)
                nargs = len(ptypes)
                if nargs > 0:
                    desc = tuple(sig.parameters.keys())
                    ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, required=arequired, help=doc)
                else:
                    ap.add_argument(f'--{arg}', action='store_true', help=doc)
        if needarg:
            raise ValueError(f"No methods staring with {self.argadapt_prefix} found and group is required")

    @staticmethod
    def _interpret(typ,value):
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
        vals = itertools.chain(ArgparserAdapter.BOOL_YES,ArgparserAdapter.BOOL_NO)
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
                assert (len(params) == len(iparams))
                callparams = []
                for value, ptype in zip(params, iparams):
                    if ptype.annotation != ptype.empty:
                        try:
                            value = self._interpret(ptype,value)
                        except Exception as e:
                            value = self.param_conversion_exception(e, name, ptype.name, ptype.annotation, value)
                    callparams.append(value)
                method(*callparams)

    @staticmethod
    def __only_methods(x):
        return inspect.ismethod(x)
