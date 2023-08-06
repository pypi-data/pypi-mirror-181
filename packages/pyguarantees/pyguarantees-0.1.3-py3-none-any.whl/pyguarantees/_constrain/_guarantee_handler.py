from typing import Tuple, Dict, Any

from pyguarantees.constraints import Guarantee, Self, Cls, GuaranteeInternal, IsUnion
from pyguarantees import severity
from pyguarantees._constraints._util.typenames import \
    get_arg_type_name
from pyguarantees._constraints._util.error_handeling import \
    handle_error


class ParameterHandler:
    """
    Since it is possible to call functions and methods with a mixture of
    args and kwargs (and a different mixture at different calls!), and kwargs
    can be used in any order, figuring out which kwarg is given which pyguarantees
    from the function call + pyguarantees-ordering alone is impossible.

    Instead, a dict has to be created with an entry for every function and
    method. For each fct, all classes will be entered into an args-list
    responsible for handling args (the order is determined by the order in
    which the classes appear in the list given to @pyguarantees.constraints()),
    and a kwargs-dict responsible for handling kwargs (where the key is the
    name given to the pyguarantees  ->  the parameter-names and pyguarantees-names
    must match for this library to handle keyword arguments!
    """
    handles = {}

    @classmethod
    def contains(cls, fct):
        if fct in cls.handles.keys():
            return True
        return False


class ReturnHandler:
    handles = {}

    @classmethod
    def contains(cls, fct):
        if fct in cls.handles.keys():
            return True
        return False


def register_parameter_contraints(fct, self_or_cls, **constraints):
    if fct in ParameterHandler.handles.keys():
        # only need to register once
        #   -> when more than one call to @pyguarantees.constrain.parameters
        #   is made on the same function / method, only the first will be used
        #   and the rest will be ignored.
        return

    _type_check_parameter_constraints(fct, constraints)
    _type_check_self_cls(fct, self_or_cls)

    ParameterHandler.handles[fct] = {"args": [], "kwargs": {}}

    if self_or_cls is not None:
        ParameterHandler.handles[fct]["args"].append(self_or_cls)

    for parameter_name, constraint in constraints.items():
        _add_info_to_constraint(constraint, parameter_name, fct, "parameter")
        ParameterHandler.handles[fct]["args"].append(constraint)
        ParameterHandler.handles[fct]["kwargs"][constraint.parameter_name] = constraint


def register_return_constraints(fct, *constraints):
    if fct in ReturnHandler.handles.keys():
        return

    _type_check_return_constraints(fct, constraints)

    ReturnHandler.handles[fct] = []
    for constraint in constraints:
        _add_info_to_constraint(constraint, "", fct, "return")
        ReturnHandler.handles[fct].append(constraint)


def _type_check_parameter_constraints(fct, constraints):
    for parameter, constraint in constraints.items():
        _type_check_constraint(
            fct,
            parameter_name=parameter,
            decorator_name="@pg.constrain.parameters",
            constraint=constraint
        )


def _type_check_return_constraints(fct, constraints):
    for i, constraint in enumerate(constraints):
        _type_check_constraint(
            fct,
            parameter_name=f"return[{i}]",
            decorator_name="@pg.constrain.returns",
            constraint=constraint
        )


def _type_check_constraint(fct, parameter_name: str, decorator_name: str, constraint):
    if not isinstance(constraint, Guarantee):
        err_constraint = GuaranteeInternal()
        _add_info_to_constraint(err_constraint, parameter_name="", fct=fct, where="internal")
        err_constraint.error_severity = severity.ERROR

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=err_constraint,
            parameter_name=parameter_name,
            what_dict={
                "error": f"All keyword-args to {decorator_name} must be of type Guarantee.",
                "should_type": "Guarantee",
                "actual_type": f"{get_arg_type_name(constraint)}"
            }
        )


def _type_check_self_cls(fct, self_or_cls):
    if self_or_cls is not None and type(self_or_cls) not in [Self, Cls]:
        err_constraint = GuaranteeInternal()
        _add_info_to_constraint(err_constraint, "", fct, "internal")
        err_constraint.error_severity = severity.ERROR

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=err_constraint,
            parameter_name="self/cls",
            what_dict={
                "should_type": "Union[Self, Cls]",
                "actual_type": f"{get_arg_type_name(self_or_cls)}"
            }
        )


def _add_info_to_constraint(
        constraint: Guarantee,
        parameter_name: str,
        fct,
        where: str
) -> None:
    """Add the given info to the given Constraint. Add it to pyguarantees in
    IsUnion, if the Guarantee is IsUnion."""
    constraint.qualname = fct.__qualname__
    constraint.parameter_name = parameter_name
    constraint.module = fct.__module__
    constraint.where = where

    if isinstance(constraint, IsUnion):
        for g in constraint.guarantees:
            _add_info_to_constraint(g, parameter_name, fct, where)


def enforce_parameter_constraints(
        fct,
        *args,
        **kwargs
) -> Tuple[Tuple, Dict]:
    # Since the args and kwargs are potentially changed,
    # create a list and dict for returning the (changed)
    # args and kwargs.
    return_args = []
    return_kwargs = {}

    # zip ensures that this only checks the args, and in the correct order
    for constraint, arg in zip(ParameterHandler.handles[fct]["args"], args):
        return_args.append(constraint.enforce(arg))

    # Python classes that the kwargs contain no duplicates of the args
    for key, val in kwargs.items():
        constraint = ParameterHandler.handles[fct]["kwargs"][key]
        return_kwargs[key] = constraint.enforce(val)

    return tuple(return_args), return_kwargs


def enforce_return_constraints(fct, *ret_vals) -> Any:
    new_ret_vals = []
    # In case of multiple return values:
    for ret_val, constraint in zip(ret_vals, ReturnHandler.handles.get(fct)):
        new_ret_vals.append(constraint.enforce(ret_val))

    # Can be single value or multiple
    #   -> if single, just return the value, else tuple
    if len(new_ret_vals) > 1:
        return tuple(new_ret_vals)
    else:
        return new_ret_vals[0]
