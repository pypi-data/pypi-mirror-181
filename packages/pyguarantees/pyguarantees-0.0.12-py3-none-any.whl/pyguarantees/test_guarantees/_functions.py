import unittest


def enforce():
    from ._test_case import TestGuarantees
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGuarantees)
    unittest.TextTestRunner().run(suite)


def main():
    unittest.main(exit=False)
    enforce()
