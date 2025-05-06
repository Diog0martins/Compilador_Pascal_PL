import ply.yacc as yacc
from lexer.pascal_analex import tokens 


# ====== Gramática ======

start = 'Programa'

from .main_rules import * 
from .declarations import *
from .body import *

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at EOF")

# ====== ======

parser = yacc.yacc()

def rec_Parser(input_string):
    return parser.parse(input_string)
