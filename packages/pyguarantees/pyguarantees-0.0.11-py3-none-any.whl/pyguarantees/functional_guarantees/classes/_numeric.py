"""Includes the numeric classes float, int, and complex."""


from dataclasses import dataclass
from typing import Union

from ._base import TypeGuarantee
from pyguarantees.functional_guarantees.classes.util.error_handeling import \
    handle_error
from pyguarantees.functional_guarantees.classes.util.typenames import \
    get_arg_type_name
from pyguarantees.functional_guarantees.classes.util.common_checks import \
    check_type, enforce_dynamic_checks


@dataclass
class NumericGuarantee(TypeGuarantee):
    isin: list = None
    minimum: float = None
    maximum: float = None


@dataclass
class IsInt(NumericGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsInt"
        self.guaranteed_type = int

    def enforce(self, arg):
        arg = check_type(arg, self)

        _check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )

        _check_min(arg, self.minimum, self)
        _check_max(arg, self.maximum, self)

        _check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg


@dataclass
class IsFloat(NumericGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsFloat"
        self.guaranteed_type = float

    def enforce(self, arg):
        arg = check_type(arg, self)

        _check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )

        _check_min(arg, self.minimum, self)
        _check_max(arg, self.maximum, self)

        _check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg


@dataclass
class IsComplex(NumericGuarantee):
    minimum_re: float = None
    maximum_re: float = None
    minimum_im: float = None
    maximum_im: float = None

    def __post_init__(self):
        self.guarantee_name = "IsComplex"
        self.guaranteed_type = complex

    def enforce(self, arg):
        arg = check_type(arg, self)

        _check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )
        _check_min_ge_max(
            guarantee=self,
            minimum=self.minimum_re,
            maximum=self.maximum_re,
            minmax_type="re"
        )
        _check_min_ge_max(
            guarantee=self,
            minimum=self.minimum_im,
            maximum=self.maximum_im,
            minmax_type="im"
        )

        _check_min(abs(arg), self.minimum, self)
        _check_max(abs(arg), self.maximum, self)
        _check_min(arg.real, self.minimum_re, self, "re")
        _check_max(arg.real, self.maximum_re, self, "re")
        _check_min(arg.imag, self.minimum_im, self, "im")
        _check_max(arg.imag, self.maximum_im, self, "im")

        _check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg


def _check_minimum_type(
        minimum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(minimum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.minimum",
            what_dict={
                "should_type": \
                    "int" if isinstance(guarantee, IsInt) else "float",
                "actual_type": get_arg_type_name(minimum)
            }
        )


def _check_maximum_type(
        maximum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(maximum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.maximum",
            what_dict={
                "should_type": \
                    "int" if isinstance(guarantee, IsInt) else "float",
                "actual_type": get_arg_type_name(maximum)
            }
        )


def _check_min_ge_max(
        guarantee: NumericGuarantee,
        minimum: Union[int, float, complex],
        maximum: Union[int, float, complex],
        minmax_type: str = "abs"
) -> None:
    if minimum is not None and maximum is not None and minimum >= maximum:
        _check_minimum_type(minimum, guarantee)
        _check_maximum_type(maximum, guarantee)

        minimum_name = "minimum" if minmax_type == "abs" else "minimum_" + minmax_type
        maximum_name = "maximum" if minmax_type == "abs" else "minimum_" + minmax_type

        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.{minimum_name} "
                           f"and {get_arg_type_name(guarantee)}.{maximum_name}",
            what_dict={
                "error": f"{minimum_name} >= {maximum_name} ",
                "minimum": str(minimum),
                "maximum": str(maximum)
            }
        )


def _check_min(
        arg: Union[int, float, complex],
        minimum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        min_type: str = "abs"
) -> None:
    if minimum is None:
        return

    _check_minimum_type(minimum, guarantee)

    if arg < minimum:
        minimum_name = "minimum" if min_type == "abs" else "minimum_" + min_type
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{guarantee.guarantee_name}.{minimum_name}",
                minimum_name: minimum,
                "actual": arg
            }
        )


def _check_max(
        arg: Union[int, float, complex],
        maximum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        max_type: str = "abs"
) -> None:
    if maximum is None:
        return

    _check_maximum_type(maximum, guarantee)

    if arg > maximum:
        maximum_name = "maximum" if max_type == "abs" else "maximum_" + max_type
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{guarantee.guarantee_name}.{maximum_name}",
                maximum_name: maximum,
                "actual": arg
            }
        )


def _check_isin(arg: Union[int, float, complex], guarantee: NumericGuarantee):
    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.isin",
            what_dict={
                "should_type": "list",
                "actual_type": f"{get_arg_type_name(guarantee.isin)}"
            }
        )

    if arg not in guarantee.isin:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {guarantee.guarantee_name}.isin",
                "isin": guarantee.isin,
                "actual": arg
            }
        )
