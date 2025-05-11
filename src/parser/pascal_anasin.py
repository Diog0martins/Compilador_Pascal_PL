import ply.yacc as yacc
from lexer.pascal_analex2 import tokens 


# ====== Gramática ======

start = 'Programa'

from .main_rules import * 
from .declarations import *
from .declaracao_uses_rules import *
from .loops import *
from .body import *
from .atribuicoes_rules import *
from .if_condicional import *
from .condicoes_rules import *

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at EOF")

# ====== ======

parser = yacc.yacc(debug=True)

def rec_Parser(input_string):
    return parser.parse(input_string)
