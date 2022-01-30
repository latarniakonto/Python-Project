
import unittest
import context
# You should run test_expression.py from within Test folder
from expression import Expression, Variable, Constant, Add


# https://coderedirect.com/questions/89611/python-unittest-testcase-execution
# -order
# solution for executing tests in order of their declaration in the class


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
# solution for executing tests by default in order of their declaration
# in the class


class TestExpression(unittest.TestCase):

    @ordered
    def test_constant_evaluation(self):
        v = Constant(0)
        self.assertEqual(v.evaluate({}), 0)

    @ordered
    def test_variable_evaluation(self):
        v = Variable("x")
        self.assertEqual(v.evaluate({"x": 0}), 0)

    @ordered
    def test_adding_operation(self):
        e = Add(Constant(0), Constant(1))
        self.assertEqual(e.evaluate({}), 1)


if __name__ == "__main__":
    unittest.main()
