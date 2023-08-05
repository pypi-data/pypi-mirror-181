import copy
from functools import wraps
import warnings


fdata = {}   # all necessary data on guaranteed functions
classmethods = {}   # needed for @tg.guarantee_usage


def guarantee_test():
    def _fct(fct):
        global fdata
        if fct not in fdata.keys():
            _add_fct_to_fdata(fct)
        return fct
    return _fct


def guarantee_usage():
    def _fct(fct):
        global fdata, classmethods

        @wraps(fct)
        def _run(*args, **kwargs):
            # If _run in fdata, incrementing the call_counter
            #   allows @tg.implements_test_for to check if the callable was used in the test.
            # If _run is not in fdata, its callable might have been decorated with an @classmethod,
            #   in which case @tg.implements_test_for has removed _run from fdata
            #   (by calling _choose_valid_functions, where this logic is implemented) and added
            #   the corresponding classmethod. This classmethod can then be found in classmethods,
            #   and the counter incremented for correct running.
            if _run in fdata.keys():
                fdata[_run]["call_counter"] += 1
            elif _run in classmethods:
                fdata[classmethods[_run]]["call_counter"] += 1
            return fct(*args, **kwargs)

        # Add _run here because it will be executed later;
        #   but guarantee_test would add _fct -> neither would work.
        if _run not in fdata.keys():
            _add_fct_to_fdata(_run, usage_guaranteed=True)
        return _run
    return _fct


def _add_fct_to_fdata(fct: callable, usage_guaranteed: bool = False):
    global fdata

    fdata[fct] = {
        "num_tests": 0,
        "call_counter": 0,
        "num_tests_with_calls": 0,
        "usage_guaranteed": usage_guaranteed,
        "testcases_without_exec": None
    }


def implements_test_for(*functions, **kwfunctions):
    global fdata

    functions = _choose_valid_functions(*functions, **kwfunctions)

    for function in functions:
        fdata[function]["num_tests"] += 1

    def _fct(test_fct):
        def _run(*args, **kwargs):
            counts_old = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]
            ret_val = test_fct(*args, **kwargs)

            counts_new = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]

            for i, fct in enumerate(functions):
                if counts_new[i] <= counts_old[i]:
                    if fdata[fct]["testcases_without_exec"] is None:
                        fdata[fct]["testcases_without_exec"] = [test_fct]
                    else:
                        fdata[fct]["testcases_without_exec"].append(test_fct)

            return ret_val
        return _run
    return _fct


def _choose_valid_functions(*functions, **kwfunctions):
    """Add kwfunctions to functions, enable working with classmethods, only use
    callables with @guarantee_test."""
    functions = list(functions)
    functions.extend(kwfunctions.values())

    # Only handle functions and methods
    #  that have a @guarantee_test decorator.
    valid_functions = []
    for function in functions:
        if function in fdata.keys():
            valid_functions.append(function)
        else:
            valid_functions = _handle_classmethods(function, valid_functions)

    return valid_functions


def _handle_classmethods(function: callable, valid_functions: list) -> list:
    # This is meant for classmethods; in them , function is not function.__func__.
    #   @classmethod is above @tg.guarantee_tests/@tg.guarantee_usage
    #   -> function.__func__ added to fdata, not function.
    #   Fix this here and use function from now on.
    if function is not function.__func__:
        valid_functions.append(function)
        fdata[function] = copy.deepcopy(fdata[function.__func__])
        fdata.pop(function.__func__)

        # Add the relationship between function and function.__func__ to
        #   classmethods in order to allow @tg.guarantee_usage to work properly.
        global classmethods
        classmethods[function.__func__] = function
    else:
        warnings.warn(
            f"The following function was given to implements_test_for "
            f"but was not decorated with @guarantee_test: "
            f" {function.__qualname__}")

    return valid_functions
