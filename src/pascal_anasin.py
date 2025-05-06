import ply.yacc as yacc
from pascal_analex import tokens 

# === Grammar ===

def p_programa(p):
    '''
    Programa : Cabecalho Dvariaveis Corpo
             | Cabecalho Corpo
    '''
    if len(p) == 4:
        print("Found: Header, Declarations, and Body")
    else:
        print("Found: Header and Body")


def p_cabecalho(p):
    'Cabecalho : PROGRAM Programname SEMICOLON'
    print(f"Program name: {p[2]}")


def p_programname(p):
    'Programname : ID'
    p[0] = p[1]


def p_dvariaveis(p):
    'Dvariaveis : VAR Listavariaveis'
    print("Found variable declarations")


def p_listavariaveis(p):
    '''
    Listavariaveis : Listavariaveis Variaveis COLON DataStructure DELIMITER
                   | 
    '''
    pass  


def p_variaveis(p):
    '''
    Variaveis : Variaveis COMMA ID 
              | ID
    '''
    pass


def p_datastructure(p):
    '''
    DataStructure : Datatype
                  | LBRACKET Array RBRACKET OF Datatype
                  | ID
    '''
    pass


def p_datatype(p):
    'Datatype : ID'
    pass


def p_array(p):
    'Array : NUMBER RANGE NUMBER'
    pass


def p_corpo(p):
    'Corpo : BEGIN conteudo END'
    print("Found program body (skipped content)")


def p_conteudo(p):
    '''
    conteudo : 
             | conteudo ID
             | conteudo SEMICOLON
             | conteudo OTHER
    '''
    pass


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def rec_Parser(input_string):
    return parser.parse(input_string)
