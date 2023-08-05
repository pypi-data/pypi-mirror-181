from dataclasses import dataclass
from typing import Any, List, Union

from ._base import TypeGuarantee
from pyguarantees.functional_guarantees.classes.util.error_handeling import \
    handle_error
from pyguarantees.functional_guarantees.classes.util.common_checks import \
    enforce_dynamic_checks, check_type
from pyguarantees.functional_guarantees.classes.util.typenames import \
    get_arg_type_name


@dataclass
class CollectionType(TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None


@dataclass
class IsList(CollectionType):
    contains: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsList"
        self.guaranteed_type = list

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_minmax_len(arg, self)
        _check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsTuple(CollectionType):
    contains: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsTuple"
        self.guaranteed_type = tuple

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_minmax_len(arg, self)
        _check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsDict(CollectionType):
    has_keys: List[Any] = None
    has_values: List[Any] = None

    def __post_init__(self):
        self.guarantee_name = "IsDict"
        self.guaranteed_type = dict

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_minmax_len(arg, self)
        _check_has_keys_values(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsSet(CollectionType):
    contains: Any = None

    def __post_init__(self):
        self.guarantee_name = "IsSet"
        self.guaranteed_type = set

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_minmax_len(arg, self)
        _check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsFrozenSet(CollectionType):
    contains: Any = None

    def __post_init__(self):
        self.guarantee_name = "IsFrozenSet"
        self.guaranteed_type = frozenset

    def enforce(self, arg):
        arg = check_type(arg, self)
        _check_minmax_len(arg, self)
        _check_contains(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg


@dataclass
class IsRange(TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsRange"
        self.guaranteed_type = range

    def enforce(self, arg):
        arg = check_type(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


def _check_minmax_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    # if pyguarantees.warnings_only, this functon may be called even though
    #   the type-check failed --> check again and return if previous test failed
    if type(arg) is not guarantee.guaranteed_type:
        return

    _check_min_ge_max(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _min_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.minimum_len is None:
        return False

    if type(guarantee.minimum_len) is not int:
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
        return False   # in case of warning instead of exception

    return True


def _max_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.maximum_len is None:
        return False

    if type(guarantee.maximum_len) is not int:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.maximum_len",
            what_dict={
                "should_type": "int",
                "actual_type": get_arg_type_name(guarantee.minimum_len)
            }
        )
        return False   # in case of warning instead of exception

    return True


def _check_min_ge_max(guarantee: CollectionType) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if not _max_len_is_legitimate(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.minimum_len & "
                           f"{guarantee.guarantee_name}.maximum_len",
            what_dict={
                "error": f"minimum_len >= maximum_len ({guarantee.minimum_len} "
                         f"> {guarantee.maximum_len}"
            }
        )


def _check_min_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _min_len_is_legitimate(guarantee):
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
                "should_len": guarantee.minimum_len,
                "actual_len": len(arg)
            }
        )


def _check_max_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _max_len_is_legitimate(guarantee):
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
                "should_len": guarantee.maximum_len,
                "actual_len": len(arg)
            }
        )


def _check_contains(
        arg: Union[list, tuple, set, frozenset],
        guarantee: Union[IsList, IsTuple, IsSet, IsFrozenSet]
) -> None:
    if type(arg) is not guarantee.guaranteed_type:
        return

    if guarantee.contains is None:
        return

    missing = []

    for item in guarantee.contains:
        if item not in arg:
            missing.append(item)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{guarantee.guarantee_name}.contains",
                "missing": missing
            }
        )


def _check_has_keys_values(
        arg: dict,
        guarantee: IsDict
) -> None:
    if type(arg) is not guarantee.guaranteed_type:
        return

    _check_has_keys(arg, guarantee)
    _check_has_values(arg, guarantee)


def _check_has_keys(arg: dict, guarantee: IsDict) -> None:
    if guarantee.has_keys is None:
        return

    missing = []
    for key in guarantee.has_keys:
        if key not in arg.keys():
            missing.append(key)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {guarantee.guarantee_name}.has_keys",
                "missing": missing
            }
        )


def _check_has_values(arg: dict, guarantee: IsDict) -> None:
    if guarantee.has_values is None:
        return

    missing = []
    for val in guarantee.has_values:
        if val not in arg.values():
            missing.append(val)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {guarantee.guarantee_name}.has_values",
                "missing": missing
            }
        )

