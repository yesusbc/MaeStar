# Avail
avail = ['T'+str(i) for i in range(1, 100)]
avail_dict = dict()


class Quadruple:
    """
    The Quadruple object contains the list of quadruples and helper functions
    """
    def __init__(self):
        self.quadruple_number = 0
        self.quadruple_dict = dict()

    def square(self, op_code, operand1, operand2, result):
        self.quadruple_dict[self.quadruple_number] = [op_code, operand1, operand2, result]
        self.quadruple_number += 1

    def get_num(self):
        return self.quadruple_number


def get_avail():
    """
    :return: Return the list of avails used
    """
    print("\n\n"+"*"*20 + "\n" + "Avail Dict: " + "\n"+"*"*20)
    print(avail_dict)


def generate_quadruple(p, square_obj, operand_stack):
    """
    :param p: p object, obtaine from Yacc
    :param square_obj: square_obj of class Quadruple
    :param operand_stack: a list, representing the stack of operands
    :return: a generated quadruple
    """
    operand2 = operand_stack.pop()              # op2 = pop operand stack
    operand1 = operand_stack.pop()              # op1 = pop operand stack
    temporal = avail.pop(0)                     # Tr = Temporal avail
    avail_dict[temporal] = operand1 + operand2  # Tr = op1 + op2

    # op_code, operand1, operand2, result
    square_obj.square(p[2], operand1, operand2, temporal)       # Save square

    operand_stack.append(temporal)              # push to operand stack Tr

    # If op1 or op2 are temporal, return them to avail
    if operand1 in avail_dict or operand2 in avail_dict:
        avail.append(temporal)
        del avail_dict[temporal]


def generate_quadruple_for(p, square_obj, operand_stack):
    """
    :param p: p object, obtaine from Yacc
    :param square_obj: square_obj of class Quadruple
    :param operand_stack: a list, representing the stack of operands
    :return: a generated quadruple specifically for For Loop
    """
    operand2 = operand_stack.pop()              # op2 = pop operand stack
    operand1 = operand_stack.pop()              # op1 = pop operand stack
    temporal = avail.pop(0)                     # Tr = Temporal avail
    avail_dict[temporal] = operand1 + operand2  # Tr = op1 + op2

    # op_code, operand1, operand2, result
    square_obj.square(p[2], operand1, operand2, temporal)       # Save square
    square_obj.square('gotoF', temporal, '_', '_')

    # If op1 or op2 are temporal, return them to avail
    if operand1 in avail_dict or operand2 in avail_dict:
        avail.append(temporal)
        del avail_dict[temporal]


def generate_quadruple_inc_dec(p, square_obj, operand_stack):
    """
    :param p: p object, obtaine from Yacc
    :param square_obj: square_obj of class Quadruple
    :param operand_stack: a list, representing the stack of operands
    :return: a generated quadruple specifically for ++ / --
    """
    operand2 = '1'              # op2 = pop operand stack
    operand1 = operand_stack.pop()              # op1 = pop operand stack
    temporal = avail.pop(0)                     # Tr = Temporal avail
    avail_dict[temporal] = operand1 + operand2  # Tr = op1 + op2

    # op_code, operand1, operand2, result
    square_obj.square(p[2], operand1, operand2, temporal)       # Save square
    square_obj.square('=', temporal, '_', operand1)       # Save square