import ply.yacc as yacc
from lexer.pascal_analex import tokens 


# ====== Gramática ======

start = 'Programa'

from .atribuicoes_rules import *
from .main_rules import * 
from .declarations import *
from .funcoes_rules import *
from .declaracao_uses_rules import *
from .body import *
from .loops import *
from .if_condicional import *
from .condicoes_rules import *

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
        print(f'Line number : {p.lineno}')
    else:
        print("Syntax error at EOF")

# ====== ======

parser = yacc.yacc(debug=True)

def rec_Parser(input_string):
    result = parser.parse(input_string)
    print(result)
    return result
