import ply.lex as lex


# Quadruple
operand_stack = list()

# Variable Tables
variable_tables = dict()
int_set = set()
double_set = set()

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
    operand_stack.append(t.value)
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
