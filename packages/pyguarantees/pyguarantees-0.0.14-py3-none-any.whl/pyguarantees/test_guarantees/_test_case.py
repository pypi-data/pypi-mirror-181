import unittest
import pytest

from pyguarantees.test_guarantees import exceptions
from ._decorators import fdata


class TestGuarantees(unittest.TestCase):
    def test_all_tests_implemented(self):
        test_all_tests_implemented()

    def test_functions_used_in_tests(self):
        test_functions_used_in_tests()


@pytest.mark.order(-2)
def test_all_tests_implemented():
    failed_fcts = []
    for fct in fdata.keys():
        if fdata[fct]["num_tests"] == 0:
            failed_fcts.append(fct)

    if failed_fcts:
        raise exceptions.TestsNotImplementedError(failed_fcts)


@pytest.mark.order(-1)
def test_functions_used_in_tests():
    failed_fcts = []
    for fct in fdata.keys():
        if fdata[fct]["usage_guaranteed"] and \
                fdata[fct]["testcases_without_exec"] is not None:
            failed_fcts.append(fct)

    if failed_fcts:
        raise exceptions.NotUsedInTestsError(failed_fcts)
