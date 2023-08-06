import pytest
from pyguarantees.testcase import fdata
import pyguarantees as pg


@pytest.mark.order(-2)
def test_all_tests_implemented():
    failed_fcts = []
    for fct in fdata.keys():
        if fdata[fct]["num_tests"] == 0:
            failed_fcts.append(fct)

    if failed_fcts:
        raise pg.exceptions.testcase.TestsNotImplementedError(failed_fcts)


@pytest.mark.order(-1)
def test_functions_used_in_tests():
    failed_fcts = []
    for fct in fdata.keys():
        if fdata[fct]["usage_guaranteed"] and \
                fdata[fct]["testcases_without_exec"] is not None:
            failed_fcts.append(fct)

    if failed_fcts:
        raise pg.exceptions.testcase.NotUsedInTestsError(failed_fcts)