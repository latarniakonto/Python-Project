import unittest
# You should run test_suite.py from within Test folder
from test_expression import TestExpression
from test_expression_data_base import TestExpressionDataBase


if __name__ == "__main__":
    suite_list = []
    suite_list. \
        append(unittest.TestLoader().loadTestsFromTestCase(TestExpression))
    suite_list. \
        append(unittest.TestLoader().
               loadTestsFromTestCase(TestExpressionDataBase))

    suite = unittest.TestSuite(suite_list)
    unittest.TextTestRunner(verbosity=3).run(suite)
