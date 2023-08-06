import unittest
import pyguarantees as pg


class TestGuarantees(unittest.TestCase):
    def test_all_tests_implemented(self):
        pg.pytests.test_all_tests_implemented()

    def test_functions_used_in_tests(self):
        pg.pytests.test_functions_used_in_tests()


def enforce():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGuarantees)
    unittest.TextTestRunner().run(suite)


def main():
    unittest.main(exit=False)
    enforce()
