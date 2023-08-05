from .error_handeling import handle_error
from .typenames import get_arg_type_name, get_type_name
from typing import Callable, List


def check_type(arg, guarantee):
    if isinstance(arg, guarantee.guaranteed_type):
        return arg

    if guarantee.force_conversion:
        try:
            return guarantee.guaranteed_type(arg)
        except TypeError:
            pass
        except ValueError:
            pass

    # Type error occurred
    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": get_type_name(guarantee.guaranteed_type),
            "actual_type": get_arg_type_name(arg),
            "force_conversion": guarantee.force_conversion
        }
    )

    return arg   # in case of warnings_only


def enforce_dynamic_checks(arg, guarantee) -> None:
    if guarantee.dynamic_checks is None:
        return

    errors = [dg for dg in guarantee.dynamic_checks if not dg.check(arg)]

    if not errors:
        return

    # Use custom error handles
    for err in errors:
        if err.callback is not None:
            err.callback(arg)

    # Show error if callbacks didn't exist or didn't stop execution
    handle_error(
        where=guarantee.where,
        type_or_value="value",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict=_get_what_dict(arg, guarantee, errors)
    )


def _get_what_dict(arg, guarantee, errors: list):
    what_dict = {
        "error": f"violated {guarantee.guarantee_name}.check_functions",
        "violations": {},
        "arg": arg
    }

    for i, error in enumerate(errors):
        key = f"check {i}"
        key = key + f" (called callback {error.callback.__name__})" if error.callback is not None else key
        val = error.description if error.description != "" else "fail"

        what_dict["violations"][key] = val

    return what_dict
