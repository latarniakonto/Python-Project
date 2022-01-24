from expression import (
    Constant, Variable,
    Add, Subtract, Times, Divide,
    Instruction, Assign, While, If
)


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
