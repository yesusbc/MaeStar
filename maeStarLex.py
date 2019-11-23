import ply.lex as lex
import quadruple

square_obj = quadruple.Quadruple()

# Quadruple
operand_stack = list()

# Variable Tables
variable_tables = dict()

# Procedure directory
procedure_directory = dict()

# Sets for saving the line number of different variables
int_set = set()
double_set = set()
method_set = set()


# List of token names
tokens = [ 'ID', 'CONST', 'MINUS', 'DIVISION', 'TIMES', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
           'LBRACKET', 'RBRACKET','LESSTHAN', 'GREATERTHAN', 'EQUALS','COMA', 'SEMICOLON',
           'ASSIGN', 'PLUSPLUS', 'MINUSMINUS']


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
            'plus': 'PLUS',
            'and': 'AND',
            'or': 'OR'
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
t_ASSIGN = r'\='
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
    line_number = t_dict['lineno']
    value = t_dict['value']

    if t.value in reserved:
        t.type = reserved[t.value]
        if value == 'method':
            method_set.add(t_dict['lineno'])
        if value == 'main':
            if len(method_set) > 0:
                num = square_obj.get_num()
                square_obj.quadruple_dict[0].pop()
                square_obj.quadruple_dict[0].append(num + 1)
    else:
        operand_stack.append(value)             # Push "operand's stack" (id)

        if line_number in int_set:
            if value not in variable_tables:
                variable_tables[line_number] = [['int', 0],['symbol', value]]

        elif line_number in double_set:
            if value not in variable_tables:
                variable_tables[line_number] = [['doubles', 0],['symbol', value]]

        elif line_number in method_set:
            operand_stack.pop()
            if len(method_set) == 1:
                square_obj.square("goto", '_', '_', '_')
            procedure_directory[value] = square_obj.get_num()
            # print(procedure_directory)
    return t


# A regular expression rule for CONSTANTS (NUMBERS)
def t_CONST(t):
    r'\d+'
    operand_stack.append(t.value)
    t.value = int(t.value)
    if t.__dict__['lineno'] in int_set:
        if len(variable_tables[t.__dict__['lineno']]) < 3:
            # [0] * t.value  First Dimension
            variable_tables[t.__dict__['lineno']][0][1] = [variable_tables[t.__dict__['lineno']][0][1]]*t.value
            operand_stack.pop()
        else:
            # [0,0,0] * t.value Multiple Dimension
            variable_tables[t.__dict__['lineno']][0][1] = [variable_tables[t.__dict__['lineno']][0][1]]*t.value
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
    # print(operand_stack)
    # for x in square_obj.quadruple_dict:
    #     print(square_obj.quadruple_dict[x])
    # print("********")


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
""" ************For testing the lexer give the lexer some input************
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
