"""Defines the @pyguarantees.functional_guarantees decorator."""


from functools import wraps

from pyguarantees._constrain._guarantee_handler import \
    enforce_parameter_constraints, ParameterHandler, \
    ReturnHandler, enforce_return_constraints, \
    register_parameter_contraints, register_return_constraints
from pyguarantees import settings


def parameters(self_or_cls=None, /, **constraints):
    def _fct(fct):
        @wraps(fct)
        def _enforce(*args, **kwargs):
            if not settings.ACTIVE:
                return fct

            if not ParameterHandler.contains(fct) and constraints is not None:
                register_parameter_contraints(fct, self_or_cls, **constraints)

            if constraints:
                args, kwargs = enforce_parameter_constraints(fct, *args, **kwargs)

            if not settings.CACHE:
                ParameterHandler.handles = {}

            return fct(*args, **kwargs)

        return _enforce
    return _fct


def returns(*constraints):
    def _fct(fct):
        @wraps(fct)
        def _enforce(*args, **kwargs):
            if not settings.ACTIVE:
                return fct

            if not ReturnHandler.contains(fct) and constraints is not None:
                register_return_constraints(fct, *constraints)

            ret_val = fct(*args, **kwargs)
            if constraints:
                if len(constraints) > 1:   # Multiple constraints -> multiple return values
                    ret_val = enforce_return_constraints(fct, *ret_val)
                else:
                    ret_val = enforce_return_constraints(fct, ret_val)

            if not settings.CACHE:
                ReturnHandler.handles = {}

            return ret_val
        return _enforce
    return _fct
