"""Defines the @pyguarantees.functional_guarantees decorator."""


from functools import wraps

from ._util import ismethod
from ._guarantee_handler import enforce_parameter_guarantees, \
    register_parameter_guarantees, ParameterHandler, \
    register_return_guarantees, ReturnHandler, \
    enforce_return_guarantees
from . import settings


def add_guarantees(
        param_guarantees=None,
        return_guarantee=None,
        is_staticmethod: bool = False
):
    def _fct(fct):
        if not settings.ACTIVE:
            return fct

        if not ParameterHandler.contains(fct) and param_guarantees is not None:
            register_parameter_guarantees(fct, param_guarantees)

        if not ReturnHandler.contains(fct) and return_guarantee is not None:
            register_return_guarantees(fct, return_guarantee)

        @wraps(fct)
        def _enforce(*args, **kwargs):
            if not settings.ACTIVE:
                return fct

            if param_guarantees is not None:
                args, kwargs = _enforce_parameter_guarantees(
                    fct, is_staticmethod, *args, **kwargs)

            ret_val = fct(*args, **kwargs)
            if return_guarantee is not None:
                ret_val = enforce_return_guarantees(fct, ret_val)

            if not settings.CACHE:
                ParameterHandler.handles = {}
                ReturnHandler.handles = {}

            return ret_val

        return _enforce
    return _fct


def _enforce_parameter_guarantees(fct, is_staticmethod, *args, **kwargs):
    """
    If a function is actually a method, the first arg will be self or cls.
    Accordingly, the first Guarantee will try to enforce itself on self or cls,
    which will inevitably fail, and the other Guarantees will be shifted on the
    args, which is of course wrong as well.

    Therefore, it is necessary to find out if a function is actually a method
    and, if it is, take this into consideration.
    """
    if ismethod(fct) and not is_staticmethod:
        # Idea:
        #   With args = [self, ...] or [cls, ...]:
        #       1.  Split args into [self] (or [cls]) and [...]
        #       2.  enforce args & kwargs
        #       3.  Remerge args with self or cls so that the function will
        #             be called correctly.
        self_or_cls = [args[0]]
        args = tuple(list(args)[1:])
        args, kwargs = enforce_parameter_guarantees(fct, *args, **kwargs)
        self_or_cls.extend(list(args))
        args = tuple(self_or_cls)
    else:
        args, kwargs = enforce_parameter_guarantees(fct, *args, **kwargs)

    return args, kwargs


