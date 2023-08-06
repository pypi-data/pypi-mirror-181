from typing import Union

from pyguarantees._constraints._util.error_handeling import \
    handle_error
from pyguarantees._constraints._util.typenames import \
    get_arg_type_name


def check_minmax_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee
) -> None:
    # if pyguarantees.warnings_only, this functon may be called even though
    #   the type-check failed --> check again and return if previous test failed
    if type(arg) is not guarantee.guaranteed_type:
        return

    _check_min_ge_max(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)

def _min_len_is_legitimate(guarantee) -> bool:
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


def _max_len_is_legitimate(guarantee) -> bool:
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


def _check_min_ge_max(guarantee) -> None:
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
        guarantee
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
        guarantee
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


def check_contains(
        arg: Union[list, tuple, set, frozenset],
        guarantee
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


def check_has_keys_values(
        arg: dict,
        guarantee
) -> None:
    if type(arg) is not guarantee.guaranteed_type:
        return

    _check_has_keys(arg, guarantee)
    _check_has_values(arg, guarantee)


def _check_has_keys(arg: dict, guarantee) -> None:
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


def _check_has_values(arg: dict, guarantee) -> None:
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