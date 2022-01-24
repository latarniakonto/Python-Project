
documentation="""
For expressions
Constant(value) - It creates constant for given value. value should be of type int
Variable(name) - It creates variable for given name. name should be of type str, it can't consists numbers.
Add(left, right) and Subtract(left, right) and Times(left, right) and Divide(left, right) - It binds two operands together using appropriate operator. Operators cannot be added/multiplied
                                                                                            left and right should be instances of Expression class.

For programming part (ex1a)
I am using expressions in implementing Instruction(first, second=None), Assign(name, value), While(condition, instructions), If(condition, yes, no)
Instruction(first, second) - first and second are instances of class Instruction e.g. While, If, Assign.
                             With introduction of Instruction class I can easily creates next "lines of code" in my custom programming language.
                             If second is None that means there are no more instructions to execute.                             
Assign(name, value) - name should be instance of Variable class. value should be instance of Constant class

While(condition, instructions) - condition should be instance of Expression class. instruction should be instance of Instruction class

If(condition, yes, no) - condition should be instance of Expression class. yes should be instance of Instruction class. no should be instance of Instruction class
                         yes is run when condition is true, no is run when condition is false.
"""


class WrongTypeException(Exception):
    pass


class WrongVariableFormatException(Exception):
    pass


class OperandNotSupportedException(Exception):
    pass


class DivisionByZeroException(Exception):
    pass


class WrongInstanceException(Exception):
    pass


class Expression:
    def __init__(self):        
        pass

    def evaluate(self, variables):
        return self.evaluate(variables)

    def __str__(self):
        return str(self)

    def __add__(w1, w2):
        return Add(w1, w2)

    def __mul__(w1, w2):
        return Times(w1, w2)


class Constant(Expression):
    def __init__(self, value):
        if not isinstance(value, int):
            raise WrongTypeException("Constant should be of type int")
        self.value = value
        self.class_name = "Constant"
        self.decoding_helper = -1

    def evaluate(self, variables):
        return self.value

    def __str__(self):
        return str(self.value)

    def __add__(w1, w2):
        return Constant(w1.value + w2.value)

    def __mul__(w1, w2):
        return Constant(w1.value * w2.value)


class Variable(Expression):
    def __init__(self, name):
        if not isinstance(name, str):
            raise WrongTypeException("Variable should be of type str")
        for letter in name:
            if letter.isnumeric():
                raise WrongVariableFormatException("Variable should consists of single letters")

        self.name = name
        self.class_name = "Variable"
        self.decoding_helper = -1

    def evaluate(self, variables):
        name = self.name

        for variable in variables:
            while variable in name:
                name = name.replace(variable, str(variables[variable]))

        return eval(name)

    def __str__(self):
        return self.name

    def __add__(w1, w2):
        return Variable(w1.name + " + " + w2.name)

    def __mul__(w1, w2):
        return Variable(w1.name + " * " + w2.name)


class Add(Expression):
    def __init__(self, left, right):
        if not isinstance(left, Expression) or not isinstance(right, Expression):
            raise WrongInstanceException("Operands should be isntances of Expression")
        self.left = left
        self.right = right
        self.class_name = "Add"
        self.decoding_helper = -1

    def evaluate(self, variables):
        return self.left.evaluate(variables) + self.right.evaluate(variables)

    def __str__(self):
        if isinstance(self.left, Variable) or isinstance(self.left, Constant):
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return str(self.left) + " + " + str(self.right)
            else:
                return str(self.left) + " + " + "(" + str(self.right) + ")"
        else:
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return "(" + str(self.left) + ")" + " + " + str(self.right)
            else:
                return "(" + str(self.left) + ")" + " + " + "(" + str(self.right) + ")"

    def __add__(w1, w2):
        raise OperandNotSupportedException("You can't add operands")

    def __mul__(w1, w2):
        raise OperandNotSupportedException("You can't multiply operands")


class Subtract(Expression):
    def __init__(self, left, right):
        if not isinstance(left, Expression) or not isinstance(right, Expression):
            raise WrongInstanceException("Operands should be isntances of Expression")
        self.left = left
        self.right = right
        self.class_name = "Subtract"
        self.decoding_helper = -1

    def evaluate(self, variables):
        return self.left.evaluate(variables) - self.right.evaluate(variables)

    def __str__(self):
        if isinstance(self.left, Variable) or isinstance(self.left, Constant):
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return str(self.left) + " - " + str(self.right)
            else:
                return str(self.left) + " - " + "(" + str(self.right) + ")"
        else:
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return "(" + str(self.left) + ")" + " - " + str(self.right)
            else:
                return "(" + str(self.left) + ")" + " - " + "(" + str(self.right) + ")"

    def __add__(w1, w2):
        raise OperandNotSupportedException("You can't add operands")

    def __mul__(w1, w2):
        raise OperandNotSupportedException("You can't multiply operands")


class Times(Expression):
    def __init__(self, left, right):
        if not isinstance(left, Expression) or not isinstance(right, Expression):
            raise WrongInstanceException("Operands should be isntances of Expression")
        self.left = left
        self.right = right
        self.class_name = "Times"
        self.decoding_helper = -1

    def evaluate(self, variables):
        return self.left.evaluate(variables) * self.right.evaluate(variables)

    def __str__(self):
        if isinstance(self.left, Variable) or isinstance(self.left, Constant):
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return str(self.left) + " * " + str(self.right)
            else:
                return str(self.left) + " * " + "(" + str(self.right) + ")"
        else:
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return "(" + str(self.left) + ")" + " * " + str(self.right)
            else:
                return "(" + str(self.left) + ")" + " * " + "(" + str(self.right) + ")"

    def __add__(w1, w2):
        raise OperandNotSupportedException("You can't add operands")

    def __mul__(w1, w2):
        raise OperandNotSupportedException("You can't multiply operands")


class Divide(Expression):
    def __init__(self, left, right):
        if not isinstance(left, Expression) or not isinstance(right, Expression):
            raise WrongInstanceException("Operands should be isntances of Expression")
        self.left = left
        self.right = right
        self.class_name = "Divide"
        self.decoding_helper = -1

    def evaluate(self, variables):
        if self.right.evaluate(variables) == 0:
            raise DivisionByZeroException("Division by zero encountered")
        return self.left.evaluate(variables) / self.right.evaluate(variables)

    def __str__(self):
        if isinstance(self.left, Variable) or isinstance(self.left, Constant):
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return str(self.left) + " / " + str(self.right)
            else:
                return str(self.left) + " / " + "(" + str(self.right) + ")"
        else:
            if isinstance(self.right, Variable) or isinstance(self.right, Constant):
                return "(" + str(self.left) + ")" + " / " + str(self.right)
            else:
                return "(" + str(self.left) + ")" + " / " + "(" + str(self.right) + ")"

    def __add__(w1, w2):
        raise OperandNotSupportedException("You can't add operands")

    def __mul__(w1, w2):
        raise OperandNotSupportedException("You can't multiply operands")


class Instruction():
    def __init__(self, first, second=None):
        if not isinstance(first, Instruction) or (second is not None and not isinstance(second, Instruction)):
            raise WrongInstanceException()
        self.first = first
        self.second = second
        self.class_name = "Instruction"
        self.decoding_helper = -1

    def run(self, variables):
        self.first.run(variables)

        if self.second is None:
            return
        self.second.run(variables)

    def __str__(self):
        if self.second is None:
            return str(self.first)
        return str(self.first) + "\n" + str(self.second)


class Assign(Instruction):
    def __init__(self, name, value):
        if not isinstance(name, Variable) or not isinstance(value, Expression):
            raise WrongInstanceException()
        self.name = name
        self.value = value
        self.class_name = "Assign"
        self.decoding_helper = -1

    def run(self, variables):
        variables[str(self.name)] = (int(str(self.value.evaluate(variables))))

    def __str__(self):
        return str(self.name) + " = " + str(self.value)


class While(Instruction):
    def __init__(self, condition, instructions):
        if not isinstance(condition, Expression) or not isinstance(instructions, Instruction):
            raise WrongInstanceException()
        self.condition = condition
        self.instructions = instructions
        self.class_name = "While"
        self.decoding_helper = -1

    def run(self, variables):
        while self.condition.evaluate(variables) != 0:
            self.instructions.run(variables)

    def __str__(self):
        return "while " + str(self.condition) + " != 0:" + "\n" + "    " + str(self.instructions)


class If(Instruction):
    def __init__(self, condition, yes, no):
        if not isinstance(condition, Expression) or not isinstance(yes, Instruction) or not isinstance(no, Instruction):
            raise WrongInstanceException()
        self.condition = condition
        self.yes = yes
        self.no = no
        self.class_name = "If"
        self.decoding_helper = -1

    def run(self, variables):
        if self.condition.evaluate(variables) != 0:
            self.yes.run(variables)
        else:
            self.no.run(variables)

    def __str__(self):
        return "if " + str(self.condition) + " != 0:\n" + "    " + str(self.yes) + "\nelse:\n" + "    " + str(self.no)

def encode_expression(e):
    if e is None:
        return "_n:"
    if e.class_name == "Constant":
        return "_c" + str(e) + ":"
    if e.class_name == "Variable":
        return "_v" + str(e) + ":"
    if e.class_name == "Instruction":
        return "_I" + encode_expression(e.first) + encode_expression(e.second)
    if e.class_name == "Assign":
        return "_=" + str(e.name) + ":" + encode_expression(e.value)
    if e.class_name == "While":
        return "_w" + encode_expression(e.condition) + encode_expression(e.instructions)
    if e.class_name == "If":
        return "_i" + encode_expression(e.condition) + encode_expression(e.yes) + encode_expression(e.no)
    if e.class_name == "Add":
        return "_+" + encode_expression(e.left) + encode_expression(e.right)
    if e.class_name == "Subtract":
        return "_-" + encode_expression(e.left) + encode_expression(e.right)
    if e.class_name == "Times":
        return "_*" + encode_expression(e.left) + encode_expression(e.right)
    if e.class_name == "Divide":
        return "_/" + encode_expression(e.left) + encode_expression(e.right)            
    raise Exception("You can't encode " + str(typeof(e)))
    

def decode_expression(code):
    # TODO
    # if code[:2] == "_n":
    #     pass
    if code[:2] == "_c":        
        end = code[2:].find(":")
        if end < 0:
            raise Exception("Decoding helper was not found")
        end += 2        
        value = int(code[2:end])        
        c = Constant(value)
        c.decoding_helper = end + 1        
        return c

    if code[:2] == "_v":        
        end = code[2:].find(":")
        if end < 0:
            raise Exception("Decoding helper was not found")
        end += 2
        name = code[2:end]
        v = Variable(name)
        v.decoding_helper = end + 1
        return v

    if code[:2] == "_I":
        first = decode_expression(code[2:])        
        second = decode_expression(code[2 + first.decoding_helper:])        
        i = Instruction(first, second)
        i.decoding_helper = first.decoding_helper + second.decoding_helper + 2
        return i            
    if code[:2] == "_=":        
        end = code[2:].find(":")
        if end < 0:
            raise Exception("Assign's name was not found")
        end += 2
        name = Variable(code[2:end])
        end += 1
        value = decode_expression(code[end:])        
        a = Assign(name, value)
        a.decoding_helper = end + value.decoding_helper
        return a        
    if code[:2] == "_w":
        condition = decode_expression(code[2:])
        instructions = decode_expression(code[2 + condition.decoding_helper:])
        w = While(condition, instructions)
        w.decoding_helper = condition.decoding_helper + instructions.decoding_helper + 2
        return w
    if code[:2] == "_i":        
        condition = decode_expression(code[2:])
        yes = decode_expression(code[2 + condition.decoding_helper:])        
        no = decode_expression(code[2 + condition.decoding_helper + yes.decoding_helper:])        
        i = If(condition, yes, no)
        i.decoding_helper = condition.decoding_helper + yes.decoding_helper + no.decoding_helper + 2
        return i

    if code[:2] == "_+":
        left = decode_expression(code[2:])
        right = decode_expression(code[2 + left.decoding_helper:])
        a = Add(left, right)
        a.decoding_helper = left.decoding_helper + right.decoding_helper + 2
        return a
        
    if code[:2] == "_-":
        left = decode_expression(code[2:])
        right = decode_expression(code[2 + left.decoding_helper:])
        s = Subtract(left, right)
        s.decoding_helper = left.decoding_helper + right.decoding_helper + 2
        return s

    if code[:2] == "_*":
        left = decode_expression(code[2:])
        right = decode_expression(code[2 + left.decoding_helper:])
        t = Times(left, right)
        t.decoding_helper = left.decoding_helper + right.decoding_helper + 2
        return t

    if code[:2] == "_/":
        left = decode_expression(code[2:])
        right = decode_expression(code[2 + left.decoding_helper:])
        d = Divide(left, right)
        d.decoding_helper = left.decoding_helper + right.decoding_helper + 2
        return d

exp1 = Divide(Times(Subtract(Variable("x"), Constant(1)),
                    Variable("x")), 
                Constant(2))
print(str(exp1))

print(encode_expression(exp1))

exp1 = decode_expression(encode_expression(exp1))
print(str(exp1))
    

inst = Instruction(Assign(Variable("x"), Constant(-4)), 
                    If(Variable("x"), 
                        Assign(Variable("x"), Constant(3)), 
                        Assign(Variable("x"), Constant(100))))
print(str(inst))
print(encode_expression(inst))

inst = decode_expression(encode_expression(inst))
print(str(inst))

inst = Instruction(
    Assign(Variable("x"), Constant(-10)), 
    While(
        Add(Variable("x"), Constant(5)), 
        Assign(Variable("x"), Add(Variable("x"), Constant(1)))))
print(str(inst))
print(encode_expression(inst))
inst = decode_expression(encode_expression(inst))
print(str(inst))

inst = Instruction(Assign(Variable("x"), Constant(3)), Assign(Variable("x"), Add(Variable("x"), Constant(1))))