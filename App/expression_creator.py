# You create your expressions and put them into database here
from expression import (
    Constant, Variable,
    Add, Subtract, Times, Divide,
    Instruction, Assign, While, If
)
from expression_formatter import decode_expression, encode_expression
from expression_data_base import (
    init,
    ArithmeticExpression,
    ProgrammingExpression,
    add_arithmetic_expression,
    add_programming_expression,    
)


session = init()

if __name__ == "__main__":
    inst = Instruction(
        Assign(Variable("x"), Constant(-10)), 
        While(
            Add(Variable("x"), Constant(5)), 
            Assign(Variable("x"), Add(Variable("x"), Constant(1)))))
    inst_code = encode_expression(inst)
    session = add_programming_expression(inst_code, session)
    print(inst)

    exp1 = Divide(Times(Subtract(Variable("x"), Constant(1)),
                    Variable("x")), 
                Constant(2))
    exp1_code = encode_expression(exp1)
    print(exp1)
    session = add_arithmetic_expression(exp1_code, session)

    inst1 = Instruction(Assign(Variable("x"), Constant(-4)), 
                    If(Variable("x"), 
                        Instruction(
        Assign(Variable("x"), Constant(-10)), 
        While(
            Add(Variable("x"), Constant(5)), 
            Assign(Variable("x"), Add(Variable("x"), Constant(1))))),
                        Assign(Variable("x"), Constant(100))))
    print(inst1)
    inst_code1 = encode_expression(inst1)
    session = add_programming_expression(inst_code1, session)
    session.commit()
    session.close() 
