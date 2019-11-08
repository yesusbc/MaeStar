import quadruple
import ply.yacc as yacc
from maeStarLex import *

# Jump stack
jump_stack = list()

square_obj = quadruple.Quadruple()


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
    """ editvariables : ID ASSIGN arithexp SEMICOLON
                      | ID dimensions ASSIGN arithexp SEMICOLON
                      | incrementdecrement
    """
    if p[1]:
        re = operand_stack.pop(0)
        id1 = operand_stack.pop(0)
        square_obj.square('=', id1, '_', re)       # Save square


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
                    | FOR LPAREN ID ASSIGN CONST SEMICOLON logicexp SEMICOLON arithexp RPAREN LBRACE severalstatutes RBRACE
    """

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
    """ dimensions :  LBRACKET idconst RBRACKET dimensions
                    | LBRACKET idconst RBRACKET
    """


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
    """ methods :     METHOD ID LPAREN RPAREN LBRACE severalstatutes RBRACE methods
                    | empty

    """


def p_calling(p):
    """ calling :     CALL ID LPAREN RPAREN SEMICOLON
    """


def p_readwrite(p):
    """ readwrite :   READ LPAREN idreadingloop RPAREN SEMICOLON
                    | WRITE LPAREN writecontent RPAREN SEMICOLON
    """


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

