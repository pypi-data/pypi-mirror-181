from dataclasses import dataclass
from typing import Type, List, Union

from ._base import _Guarantee, _TypeGuarantee
from pyguarantees._constraints._util.error_handeling import \
    handle_error
from pyguarantees._constraints._util.typenames import \
    get_arg_type_name, get_type_name
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_forbidden_values


@dataclass
class _NoOp(_Guarantee):
    def __post_init__(self):
        self.guarantee_name = "NoOp"
        self.guaranteed_type = None

    def enforce(self, arg):
        return arg


@dataclass
class _Self(_NoOp):
    def __post_init__(self):
        self.guarantee_name = "Self"
        self.guaranteed_type = None


@dataclass
class _Cls(_NoOp):
    def __post_init__(self):
        self.guarantee_name = "Cls"
        self.guaranteed_type = None


@dataclass
class _IsClass(_TypeGuarantee):
    class_type: Type = None

    def __post_init__(self):
        self.guarantee_name = "IsClass"
        self.guaranteed_type = self.class_type

    def enforce(self, arg):
        arg = _check_isclass(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class _IsNone(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsNone"
        self.guaranteed_type = None

    def enforce(self, arg):
        if arg is None:
            enforce_dynamic_checks(arg, self)
            return

        handle_error(
            where=self.where,
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={
                "should_type": "None",
                "actual_type": get_arg_type_name(arg)
            }
        )


@dataclass
class _IsUnion(_TypeGuarantee):
    guarantees: List[_TypeGuarantee] = None

    def __post_init__(self):
        self.guarantee_name = "IsUnion"
        self.guaranteed_type = Union

    def enforce(self, arg):
        arg = self.__enforce_union_guarantees(arg)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg

    def __enforce_union_guarantees(self, arg):
        for guarantee in self.guarantees:
            self.__handle_noop(guarantee)
            self.__handle_isunion(guarantee)

            guarantee.qualname = f"{self.qualname}: IsUnion"
            guarantee.module = self.module

            # 1. Try to change arg to wanted type if allowed
            # 1.1  If ValueError: definitely wrong type -> continue
            # 2. Check type (whether force_conversion or not)
            # 2.1  If wrong type: loop continues or type is false
            # 2.2  If right type: enforce it

            # Different type-check for None
            if arg is guarantee.guaranteed_type is None:
                return guarantee.enforce(arg)
            elif guarantee.guaranteed_type is None:
                continue   # no conversion attempt necessary; arg should be None but isn't
            elif arg is None:
                continue   # arg should not be None but is

            # Attempt conversion
            if guarantee.force_conversion:
                try:
                    arg = guarantee.guaranteed_type(arg)   # might be int or float -> int(arg) or float(arg)
                except ValueError:
                    continue
                except TypeError:
                    continue

            if type(arg) is guarantee.guaranteed_type:
                return guarantee.enforce(arg)

        # Didn't work
        should_types = \
            [get_type_name(g.guaranteed_type) for g in self.guarantees]
        handle_error(
            where=self.where,
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={
                "should_type": f"Union{should_types}",
                "actual_type": get_arg_type_name(arg)
            }
        )

        # In case of warnings_only
        return arg

    def __handle_noop(self, guarantee):
        if not isinstance(guarantee, _NoOp):
            return

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={"error": "IsUnion may not contain NoOp."}
        )

    def __handle_isunion(self, guarantee):
        if not isinstance(guarantee, _IsUnion):
            return

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={"error": "IsUnion may not contain IsUnion."}
        )


def _check_isclass(arg: object, guarantee: _IsClass) -> object:
    if guarantee.class_type is None or isinstance(arg, guarantee.class_type):
        return arg

    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": str(guarantee.class_type),
            "actual_type": get_arg_type_name(arg)
        }
    )
