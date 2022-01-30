import unittest
import sys
import context

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from io import TextIOWrapper, BytesIO
# You should run test_expression_data_base.py from within Test folder
from expression_data_base import (
    list_arithmetic_expression, list_programming_expression,
    Base, add_programming_expression, add_arithmetic_expression
)

# https://coderedirect.com/questions/89611/python-unittest-testcase-execution-
# order
# solution for executing tests in order of their declaration in the class
# It works for test_expression_data_base.py.
# It doesn't work for test_suite.py, but I think
# it is interesting so I left it here


def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare


ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare
# solution for executing tests in order of their declaration in the class
# It works for test_expression_data_base.py.
# It doesn't work for test_suite.py, but I think
# it is interesting so I left it here

# Tests should be executed by default in order of their declaration in the
# class


class TestExpressionDataBase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Output redirecting method
        # https://stackoverflow.com/questions/15940389/in-python-how-to-do-
        # unit-test-on-a-function-without-return-value
        self._old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        self._stdout = sys.stdout

    # Output redirecting method
    # https://stackoverflow.com/questions/15940389/in-python-how-to-do-
    # unit-test-on-a-function-without-return-value
    def _output(self):
        self._stdout.seek(0)
        return self._stdout.read()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        # Output redirecting method
        # https://stackoverflow.com/questions/15940389/in-python-how-to-do-
        # unit-test-on-a-function-without-return-value
        sys.stdout = self._old_stdout
        self._stdout.close()

    @ordered
    def test_list_book_empty(self):
        list_programming_expression(self.session)
        self.assertEqual(self._output(), "")

    @ordered
    def test_list_programming_expression_not_empty(self):
        add_programming_expression("""_c123:""", self.session)
        list_programming_expression(self.session)
        self.assertEqual(self._output(), """(1, '_c123:')\n""")

    @ordered
    def test_list_arithmetic_expression_empty(self):
        list_arithmetic_expression(self.session)
        self.assertEqual(self._output(), "")

    @ordered
    def test_list_arithmetic_expression_not_empty(self):
        add_arithmetic_expression("""_c123:""", self.session)
        list_arithmetic_expression(self.session)
        self.assertEqual(self._output(), """(1, '_c123:')\n""")


if __name__ == "__main__":
    unittest.main()
