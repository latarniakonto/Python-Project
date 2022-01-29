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

    exp1 = Divide(Times(Subtract(Variable("x"), Constant(1)), Variable("x")),
                  Constant(2))
    exp1_code = encode_expression(exp1)
    print(exp1)
    session = add_arithmetic_expression(exp1_code, session)

    exp2 = Add(Divide(Times(Subtract(Constant(0), Constant(22)), Constant(3)),
                      Constant(11)),
               Constant(17))
    exp2_code = encode_expression(exp2)
    print(exp2)
    session = add_arithmetic_expression(exp2_code, session)

    inst = Instruction(
        Assign(Variable("x"), Constant(-10)),
        While(
            Add(Variable("x"), Constant(5)),
            Assign(Variable("x"), Add(Variable("x"), Constant(1)))))
    inst_code = encode_expression(inst)
    session = add_programming_expression(inst_code, session)
    print(inst)

    inst1 = Instruction(Assign(Variable("x"), Constant(-4)),
                        If(Variable("x"),
                        Instruction(
                            Assign(Variable("x"), Constant(-10)),
                            While(
                                Add(Variable("x"), Constant(5)),
                                Assign(Variable("x"), Add(Variable("x"),
                                       Constant(1))))),
                        Assign(Variable("x"), Constant(100))))
    print(inst1)
    inst_code1 = encode_expression(inst1)
    session = add_programming_expression(inst_code1, session)

    inst2 = Instruction(
        Assign(Variable("y"), Constant(-10)),
        Instruction(Assign(Variable("x"), Constant(2)),
                    While(Variable("y"),
                          Instruction(
                              Assign(Variable("y"), Add(Variable("y"),
                                     Constant(1))),
                              Assign(Variable("x"), Times(Variable("x"),
                                     Constant(3)))))))
    inst_code2 = encode_expression(inst2)
    session = add_programming_expression(inst_code2, session)
    print(inst2)

    session.commit()
    session.close()
