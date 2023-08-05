from dataclasses import dataclass
from typing import List

from ._base import TypeGuarantee
from pyguarantees.functional_guarantees.classes.util.common_checks import \
    check_type, enforce_dynamic_checks
from pyguarantees.functional_guarantees.classes.util.error_handeling import \
    handle_error
from pyguarantees.functional_guarantees.classes.util.typenames import \
    get_arg_type_name


@dataclass
class IsStr(TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None
    isin: List = None

    def __post_init__(self):
        self.guarantee_name = "IsStr"
        self.guaranteed_type = str

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_len(arg, self)
        _check_isin(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


def _check_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:   # Can happen if pyguarantees.warnings_only is True
        return

    _check_min_len_ge_max_len(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _minimum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.minimum_len) is int:
        return True

    handle_error(
        where="internal",
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=f"{guarantee.guarantee_name}.minimum_len",
        what_dict={
            "should_type": "int",
            "actual_type": get_arg_type_name(guarantee.minimum_len)
        }
    )

    return False   # in case of warnings_only


def _maximum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.maximum_len) is int:
        return True

    handle_error(
        where="internal",
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=f"{guarantee.guarantee_name}.maximum_len",
        what_dict={
            "should_type": "int",
            "actual_type": get_arg_type_name(guarantee.maximum_len)
        }
    )

    return False   # in case of warnings_only


def _check_min_len_ge_max_len(guarantee: IsStr) -> None:
    if guarantee.minimum_len is None or guarantee.maximum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee) \
            or not _maximum_len_type_is_correct(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.minimum_len "
                           f"and {guarantee.guarantee_name}.maximum_len",
            what_dict={
                "error": "minimum_len >= maximum_len",
                "minimum_len": str(guarantee.minimum_len),
                "maximum_len": str(guarantee.maximum_len)
            }
        )


def _check_min_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.minimum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee):
        return

    if len(arg) < guarantee.minimum_len:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{guarantee.guarantee_name}.minimum_len",
                "minimum_len": str(guarantee.minimum_len),
                "actual len": str(len(arg))
            }
        )


def _check_max_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.maximum_len is None:
        return

    if not _maximum_len_type_is_correct(guarantee):
        return

    if len(arg) > guarantee.maximum_len:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{guarantee.guarantee_name}.maximum_len",
                "maximum_len": str(guarantee.maximum_len),
                "actual len": str(len(arg))
            }
        )


def _check_isin(arg: str, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

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
                "actual_type": get_arg_type_name(guarantee.isin)
            }
        )

    if arg in guarantee.isin:
        return

    handle_error(
        where=guarantee.where,
        type_or_value="value",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "error": f"violated {guarantee.guarantee_name}.isin",
            "isin": f"{guarantee.isin}",
            "actual": arg  # is str
        }
    )

