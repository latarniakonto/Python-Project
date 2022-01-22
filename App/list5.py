
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
        

    def evaluate(self, variables):
        if self.right.evaluate(variables) == 0: raise DivisionByZeroException("Division by zero encountered")
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

    def run(self, variables):
        self.first.run(variables)
        
        if self.second is None: return
        self.second.run(variables)

    def __str__(self):
        if self.second is None: return str(self.first)
        return str(self.first) + "\n" + str(self.second)

class Assign(Instruction):
    def __init__(self, name, value):
        if not isinstance(name, Variable) or not isinstance(value, Expression):
            raise WrongInstanceException()
        self.name = name
        self.value = value

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
    
    def run(self, variables):                
        if self.condition.evaluate(variables) != 0:
            self.yes.run(variables)
        else:
            self.no.run(variables)

    def __str__(self):
        return "if " + str(self.condition) + " != 0:\n" + "    " + str(self.yes) + "\nelse:\n" + "    " + str(self.no)


#Testing expressions
print("\nExpressions")
exp1 = Times(Add(Variable("x"), Constant(2)), Variable("y"))
print(exp1)
print(exp1.evaluate({"x":1, "y":21}))
exp1 = Times(Divide(Variable("x"), Constant(2)), Variable("y"))
print(exp1)
print(exp1.evaluate({"x":1, "y":21}))

# x = Constant(3)
# y = Constant(5)
# z = x + y
# print(z)
# print(z.evaluate({}))

exp1 = Subtract(Add(Constant(2), Times(Variable("x"), Constant(7))),
                Add(Times(Variable("y"), Constant(3)), Constant(5)))
print(exp1)
print(exp1.evaluate({"x":0.1, "y":100}))


# exp1 = Subtract(Add(Constant(2), Subtract(Variable("x"), Constant(7))),
#                 Add(Divide(Variable("y"), Constant(3)), Constant(5)))
# print(exp1)
# print(exp1.evaluate({"x":0.1, "y":100}))
# print(exp1.evaluate({"x":0.2, "y":100}))


exp1 = Divide(Times(Subtract(Variable("x"), Constant(1)),
                    Variable("x")), 
                Constant(2))
print(exp1)
print(exp1.evaluate({"x":11}))
#Testing programming expressions
print("\nProgramming expressions")
input_and_output = {}
inst = Instruction(Assign(Variable("x"), Constant(3)), Assign(Variable("x"), Add(Variable("x"), Constant(1))))
print(inst)
inst.run(input_and_output)
print(input_and_output["x"])

# input_and_output = {}
# inst = Instruction(Assign(Variable("x"), Constant(4)))
# print(inst)
# inst.run(input_and_output)
# print(input_and_output["x"])

inst = Instruction(
    Assign(Variable("x"), Constant(-10)), 
    While(
        Add(Variable("x"), Constant(5)), 
        Assign(Variable("x"), Add(Variable("x"), Constant(1)))))

print(inst)
input_and_output = {}
inst.run(input_and_output)
print(input_and_output["x"])

# inst = Instruction(Assign(Variable("x"), Constant(-2)), 
#                     If(Add(Variable("x"), Constant(4)), 
#                         Assign(Variable("x"), Constant(3)), 
#                         Assign(Variable("x"), Constant(100))))
# print(inst)
# input_and_output = {}
# inst.run(input_and_output)
# print(input_and_output["x"])

inst = Instruction(Assign(Variable("x"), Constant(-4)), 
                    If(Variable("x"), 
                        Assign(Variable("x"), Constant(3)), 
                        Assign(Variable("x"), Constant(100))))
print(inst)
input_and_output = {}
inst.run(input_and_output)
print(input_and_output["x"])