import ply.yacc as yacc
from maeStarLex import *

# Jump stack
jump_stack = list()
for_stack = list()

# will hold a jump stack specifically for "dimensions"
dimensions_direction = list()
# will hold the line number of the dimensions
dimensions_set = set()
# With the line number as key, it will hold the value/dimensions of the specific variable
dimensions_dict = dict()


# ---------------------------- GRAMMAR FUNCTIONS -------------------------------


def p_program(p):
    """ program : variables methods MAIN LBRACE severalstatutes RBRACE
    """


# Quitar variables????
def p_statutes(p):
    """ statutes :    conditional
                    | editvariables
                    | cyclical
                    | calling
                    | readwrite
    """


def p_editvariables(p):
    """ editvariables : singledimension
                      | multidimension
                      | incrementdecrement
    """


def p_singledimension(p):
    """ singledimension : ID ASSIGN arithexp SEMICOLON
    """
    if p[1]:
        re = operand_stack.pop(0)
        id1 = operand_stack.pop(0)
        square_obj.square('=', id1, '_', re)       # Save square


def p_multidimension(p):
    """ multidimension : ID dimensions ASSIGN arithexp SEMICOLON
    """
    # adding dimension to array variables in quadruples
    line_number = str(p.slice[1].__dict__['lineno'])

    if line_number in dimensions_dict:
        re = operand_stack.pop(0)
        id1 = operand_stack.pop()
        square_obj.square('=', id1, '_', re)

        to_add_value = dimensions_dict[line_number]
        num = square_obj.get_num() - 1
        prev_value = square_obj.quadruple_dict[num].pop()
        new_value = prev_value + to_add_value
        square_obj.quadruple_dict[num].append(new_value)    # We add the new dimension to the variable

        for _ in range(new_value.count('[')):   # We need to remove the extra operands
            operand_stack.pop()


def p_incrementdecrement(p):
    """ incrementdecrement : selectid PLUSPLUS SEMICOLON
                      | selectid MINUSMINUS SEMICOLON
    """
    if p[2] == '++':
        quadruple.generate_quadruple_inc_dec(p, square_obj, operand_stack)


def p_selectid(p):
    """ selectid :         ID
                        | ID dimensions

    """


def p_conditional(p):
    """ conditional :   IF LPAREN logicexp RPAREN ckp_if1 LBRACE severalstatutes RBRACE ckp_if3
                        | IF LPAREN logicexp RPAREN ckp_if1 LBRACE severalstatutes RBRACE elsecase
    """


def p_elsecase(p):
    """ elsecase : ELSE ckp_if2 LBRACE severalstatutes RBRACE ckp_if3
    """


def p_ckp_if1(p):
    """ ckp_if1 : empty
    """
    re = operand_stack.pop()
    square_obj.square('gotoF', re, '_', '_')
    jump_stack.append(square_obj.get_num() - 1)


def p_ckp_if2(p):
    """ ckp_if2 : empty
    """
    dir1 = jump_stack.pop()
    square_obj.square('goto', '_', '_', '_')
    num = square_obj.get_num()
    square_obj.quadruple_dict[dir1].pop()
    square_obj.quadruple_dict[dir1].append(num)
    jump_stack.append(num - 1)


def p_ckp_if3(p):
    """ ckp_if3 : empty
    """
    dir1 = jump_stack.pop()
    num = square_obj.get_num()
    square_obj.quadruple_dict[dir1].pop()
    square_obj.quadruple_dict[dir1].append(num)


def p_severalstatutes(p):
    """ severalstatutes :  statutes severalstatutes
                        | statutes
                        | empty
    """


def p_cyclical(p):
    """ cyclical :    DO ckp_dowhile1 LBRACE severalstatutes RBRACE WHILE LPAREN logicexp RPAREN ckp_dowhile2
                    | WHILE ckp_while1 LPAREN logicexp RPAREN ckp_while2 LBRACE severalstatutes RBRACE ckp_while3
                    | FOR LPAREN for1section SEMICOLON for2section SEMICOLON for3section RPAREN LBRACE severalstatutes RBRACE for4section
    """


def p_for1section(p):
    """ for1section : ID ASSIGN CONST
    """
    id_name = p.slice[1].__dict__['value']
    operation = p.slice[2].__dict__['value']
    value = p.slice[3].__dict__['value']
    square_obj.square(operation, value, '_', id_name)
    operand_stack.pop()
    operand_stack.pop()     # We're creating or own quadruple here, so we must remove the operands from the stack


def p_for2section(p):
    """ for2section : logicfunction
    """


def p_for3section(p):
    """ for3section : ID PLUSPLUS
                    | ID MINUSMINUS
                    | for3_1section
    """
    if str(p.slice[1]) != "for3_1section":
        id_name = p[1]
        operation = p[2]
        for_avail_num = len(for_stack)
        for_stack.append(('=', 'TF'+str(for_avail_num), '_', id_name))
        for_stack.append((operation, id_name, '1', 'TF'+str(for_avail_num)))
        operand_stack.pop()     # We're creating or own quadruple here, so we must remove the operands from the stack


def p_for3_1section(p):
    """ for3_1section : ID PLUS CONST
                    | ID MINUS CONST
                    | ID TIMES CONST
                    | ID DIVISION CONST
    """
    id_name = p.slice[1].__dict__['value']
    operation = p.slice[2].__dict__['value']
    value = p.slice[3].__dict__['value']
    for_avail_num = len(for_stack)
    for_stack.append(('=', 'TF'+str(for_avail_num), '_', id_name))
    for_stack.append((operation, value, id_name, 'TF'+str(for_avail_num)))
    operand_stack.pop()
    operand_stack.pop()     # We're creating or own quadruple here, so we must remove the operands from the stack


def p_for4section(p):
    """ for4section : empty
    """
    dir1 = jump_stack.pop()
    num = square_obj.get_num() + 2      # Plus 2 because of the next two quadruples we're going to add

    op_code, operand1, operand2, result = for_stack.pop()
    square_obj.square(op_code, operand1, operand2, result)

    square_obj.quadruple_dict[dir1 + 1].pop()
    square_obj.quadruple_dict[dir1 + 1].append(num)
    square_obj.square("gotoFor", '_', '_', dir1)


def p_ckp_while1(p):
    """ ckp_while1 : empty
    """
    jump_stack.append(square_obj.get_num())


def p_ckp_while2(p):
    """ ckp_while2 : empty
    """
    re = operand_stack.pop()
    square_obj.square('gotoF', re, '_', '_')
    jump_stack.append(square_obj.get_num() - 1)


def p_ckp_while3(p):
    """ ckp_while3 : empty
    """
    dir1 = jump_stack.pop()
    dir2 = jump_stack.pop()
    square_obj.square('goto', '_', '_', str(dir2))
    num = square_obj.get_num()
    square_obj.quadruple_dict[dir1].pop()
    square_obj.quadruple_dict[dir1].append(num)


def p_ckp_dowhile1(p):
    """ ckp_dowhile1 : empty
    """
    jump_stack.append(square_obj.get_num())


def p_ckp_dowhile2(p):
    """ ckp_dowhile2 : empty
    """
    re = operand_stack.pop()
    dir1 = jump_stack.pop()
    square_obj.square('gotoT', re, '_', dir1)


def p_variables(p):
    """ variables : type ID SEMICOLON variables
                    | type ID dimensions SEMICOLON
                    | empty
    """
    if str(p.slice[1]) == 'type':
        operand_stack.pop()      # These are not operands, we need to remove them at the beginning


def p_dimensions(p):
    """ dimensions :  LBRACKET CONST RBRACKET dimensions
                    | LBRACKET CONST RBRACKET
    """
    line_number = str(p.slice[1].__dict__['lineno'])
    value = str(p.slice[2].__dict__['value'])

    if line_number in dimensions_dict:
         prev_value = dimensions_dict[line_number]
         dimensions_dict[line_number] = '[' + value + ']'  + prev_value
    else:
        dimensions_dict[line_number] = '[' + value + ']'


def p_type(p):
    """ type :        INT
                    | DOUBLE
    """
    p_dict = p.slice[1].__dict__
    var_type = p_dict['value']

    if var_type == 'int':
        int_set.add(p_dict['lineno'])
    elif var_type == 'double':
        double_set.add(p_dict['lineno'])



def p_methods(p):
    """ methods :     METHOD ID LPAREN RPAREN LBRACE severalstatutes RBRACE return_method methods
                    | empty
    """

def p_return_method(p):
    """ return_method : empty
    """
    square_obj.square('Return', '.', '.', '.')


def p_calling(p):
    """ calling :     CALL ID LPAREN RPAREN SEMICOLON
    """
    method_name = p.slice[2].__dict__['value']
    square_obj.square('call', method_name, '_', procedure_directory[method_name])
    operand_stack.pop(0)


def p_readwrite(p):
    """ readwrite :   READ LPAREN idreadingloop RPAREN SEMICOLON
                    | WRITE LPAREN writecontent RPAREN SEMICOLON
    """
    while(operand_stack):
        id_name = operand_stack.pop()
        operation = p[1]
        square_obj.square(operation, '_','_', id_name)


# X : A X
# X : A
def p_idreadingloop(p):
    """ idreadingloop : ID COMA idreadingloop
                    | ID
    """



# to print messages is missing
def p_writecontent(p):
    """ writecontent : arithfunction
                     | logicfunction
    """


def p_arithexp(p):
    """ arithexp :    arithterm
                    | arithterm PLUS arithexp
                    | arithterm MINUS arithexp
    """
    if len(p) > 2:
        if str(p[2]) in ('plus', '-'):                         # ONLY FOR PLUS
            quadruple.generate_quadruple(p, square_obj, operand_stack)


def p_arithterm(p):
    """ arithterm :   arithfunction
                    | arithfunction TIMES arithterm
                    | arithfunction DIVISION arithterm
    """
    if len(p) > 2:
        if str(p[2]) in ('*', '/'):                         # ONLY FOR *
            quadruple.generate_quadruple(p, square_obj, operand_stack)


def p_arithfunction(p):
    """ arithfunction : idconst
                    | LPAREN arithexp RPAREN
    """


def p_logicexp(p):
    """ logicexp :    logicterm
                    | logicterm OR logicexp
    """
    if len(p) > 2:
        if str(p[2]) == 'or':                         # ONLY FOR /
            quadruple.generate_quadruple(p, square_obj, operand_stack)


def p_logicterm(p):
    """ logicterm :   logicfunction
                    | logicfunction AND logicterm
    """
    if len(p) > 2:
        if str(p[2]) == 'and':                         # ONLY FOR /
            quadruple.generate_quadruple(p, square_obj, operand_stack)


def p_logicfunction(p):
    """ logicfunction : idconst LESSTHAN idconst
                    | idconst GREATERTHAN idconst
                    | idconst EQUALS idconst
                    | LPAREN logicexp RPAREN
    """
    if p.__dict__['stack'][6].__dict__['value'] == 'for':
        num = square_obj.get_num()
        jump_stack.append(num)
        quadruple.generate_quadruple_for(p, square_obj, operand_stack)
    else:
        if len(p) > 2:
            if str(p[2]) in ('<', '>', '=='):
                quadruple.generate_quadruple(p, square_obj, operand_stack)


def p_idconst(p):
    """ idconst :     ID
                    | CONST
    """


def p_empty (p):
    """ empty :
    """


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def get_parser():
    """
    :return: Parser object
    """
    parser = yacc.yacc()
    return parser