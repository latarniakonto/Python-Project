# You create your expressions and put them into database here
from expression import (
    Constant, Variable,
    Add, Subtract, Times, Divide,
    Instruction, Assign, While, If
)
from expression_formatter import encode_expression
from expression_data_base import (
    init,
    ArithmeticExpression,
    ProgrammingExpression,
    add_arithmetic_expression,
    add_programming_expression,
    list_programming_expression,
    list_arithemitc_expression
)


session = init()

if __name__ == "__main__":
    inst = Instruction(
        Assign(Variable("x"), Constant(-10)), 
        While(
            Add(Variable("x"), Constant(5)), 
            Assign(Variable("x"), Add(Variable("x"), Constant(1)))))
    inst_code = encode_expression(inst)
    add_programming_expression(inst_code, session)
    list_programming_expression(session)

    exp1 = Divide(Times(Subtract(Variable("x"), Constant(1)),
                    Variable("x")), 
                Constant(2))
    exp1_code = encode_expression(exp1)
    add_arithmetic_expression(exp1_code, session)
    list_arithemitc_expression(session)    
    
    


