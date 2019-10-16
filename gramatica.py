#Author: Yesus Becerril
#ID: A00513040
#Date: September 9, 2019
#python 3

import ply.lex as lex
import ply.yacc as yacc
import sys


# Variable Tables
variable_tables = dict()
int_set = set()
double_set = set()

# Quadruple
quadruple_list = list()
operand_stack = list()

# Avail
avail = ['T'+str(i) for i in range(1, 100)]
avail_dict = dict()


class Quadruple:

    @staticmethod
    def square(op_code, operand1, operand2, result):
        quadruple_list.append((op_code, operand1, operand2, result))


square_obj = Quadruple()

# List of token names

tokens = [ 'ID', 'CONST', 'MINUS', 'DIVISION', 'TIMES', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
           'LBRACKET', 'RBRACKET','LESSTHAN', 'GREATERTHAN', 'EQUALS','COMA', 'SEMICOLON',
           'COLON', 'ASSIGN', 'AND', 'OR', 'PLUSPLUS', 'MINUSMINUS']


# Reserved words

reserved = {'if': 'IF',
            'do': 'DO',
            'while': 'WHILE',
            'main': 'MAIN',
            'for': 'FOR',
            'else': 'ELSE',
            'read': 'READ',
            'write': 'WRITE',
            'call': 'CALL',
            'int': 'INT',
            'double': 'DOUBLE',
            'method': 'METHOD',
            'plus': 'PLUS'
            }


tokens += list(reserved.values())


# Each token is specified by writing a regular expression rule compatible with Python's re module.

# t_PLUS = r'\PLUS'
t_PLUSPLUS = r'\++'
t_MINUS = r'\-'
t_MINUSMINUS = r'\--'
t_DIVISION = r'/'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN =  r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET =r'\['
t_RBRACKET = r'\]'
#t_QUOT = r'["]'
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_EQUALS = r'\=='
t_COMA = r'\,'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_ASSIGN = r'\='
t_AND = r'\&'
t_OR = r'\|'
# To ignore characters spaces and tabs
t_ignore = " \t\r"

"""
************************************************
************************************************
Regular expression rules with no action code
************************************************
************************************************
"""


# Check for reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t_dict = t.__dict__

    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        operand_stack.append(t_dict['value'])             # Push "operand's stack" (id)
        if t_dict['lineno'] in int_set:

            if t_dict['value'] not in variable_tables:
                variable_tables[t_dict['value']] = ['int', 0]

        elif t_dict['lineno'] in double_set:
            if t_dict['value'] not in variable_tables:
                variable_tables[t_dict['value']] = ['doubles', 0]

    return t


# A regular expression rule for CONSTANTS (NUMBERS)
def t_CONST(t):
    r'\d+'
    t.value = int(t.value)
    """
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large {0}".format(t.value))
        t.value = 0
    """
    return t


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

""" # For testing the lexer give the lexer some input
while True:
    # Tokenize
    print("*"*40)
    s = input()
    lexer.input(s)
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
"""


# Grammar functions
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
                        | selectid PLUSPLUS SEMICOLON
                        | selectid MINUSMINUS SEMICOLON
    """


def p_selectid(p):
    """ selectid :         ID
                        | ID dimensions

    """


def p_conditional(p):
    """ conditional :   IF LPAREN logicexp RPAREN LBRACE severalstatutes RBRACE
                        | IF LPAREN logicexp RPAREN LBRACE severalstatutes RBRACE ELSE LBRACE severalstatutes RBRACE
    """


def p_severalstatutes(p):
    """ severalstatutes :  statutes severalstatutes
                        | statutes
                        | empty
    """


def p_cyclical(p):
    """ cyclical :    DO LBRACE severalstatutes RBRACE WHILE LPAREN logicexp RPAREN
                    | WHILE LPAREN logicexp RPAREN LBRACE severalstatutes RBRACE
                    | FOR LPAREN ID ASSIGN CONST SEMICOLON logicexp SEMICOLON arithexp RPAREN LBRACE severalstatutes RBRACE
    """


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
        if str(p[2]) == 'plus':                         # ONLY FOR PLUS
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


def p_arithterm(p):
    """ arithterm :   arithfunction
                    | arithfunction TIMES arithterm
                    | arithfunction DIVISION arithterm
    """
    if len(p) > 2:
        if str(p[2]) == '*':                         # ONLY FOR *
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


def p_arithfunction(p):
    """ arithfunction : idconst
                    | ID PLUSPLUS
                    | ID MINUSMINUS
                    | LPAREN arithexp RPAREN
    """


def p_logicexp(p):
    """ logicexp :    logicterm
                    | logicterm OR logicexp
    """


def p_logicterm(p):
    """ logicterm :   logicfunction
                    | logicfunction AND logicterm
    """


def p_logicfunction(p):
    """ logicfunction : idconst LESSTHAN idconst
                    | idconst GREATERTHAN idconst
                    | idconst EQUALS idconst
                    | LPAREN logicexp RPAREN
    """


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


parser = yacc.yacc()


"""
while True:
    try:
        s = input('$ ')
    except EOFError:    #If input() didn't read any date before encountering end
        break
    parser.parse(s)
"""


# file = open('codigoprueba', 'r')
# file = open('maesumamatrices.txt', 'r')
file = open('debug.txt', 'r')
code = file.read()
print(code)
parser.parse(code)

print("\n\n"+"*"*20 + "\n" + "Cuadros: " + "\n"+"*"*20)
for cuadro in quadruple_list:
    print(cuadro)


print("\n\n"+"*"*20 + "\n" + "Avail Dict: " + "\n"+"*"*20)
print(avail_dict)


# Assigning values
# print(operand_stack)
while(operand_stack):
    value = operand_stack.pop()
    destiny = operand_stack.pop()
    variable_tables[destiny][1] = value


print("\n\n"+"*"*20 + "\n" + "Variable Tables: " + "\n"+"*"*20)
print(variable_tables)

