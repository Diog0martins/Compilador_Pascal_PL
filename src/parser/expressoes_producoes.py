from codegen.expressoes import (
    gerar_expressao_binaria,
    gerar_termo_binario,
    gerar_fator_id,
    gerar_fator_array
)

# ====== Produções de Expressões ======

def p_Expressao_complex(p):
    '''
    Expressao : Expressao '+' Termo
              | Expressao '-' Termo
    '''
    p[0] = gerar_expressao_binaria(p[1], p[2], p[3])


def p_Expressao(p):
    '''
    Expressao : Termo
    '''
    p[0] = p[1]


def p_termo_complex(p):
    '''
    Termo : Termo '*' Fator
          | Termo MOD Fator
          | Termo DIV Fator
    '''
    p[0] = gerar_termo_binario(p[1], p[2], p[3])


def p_termo_simple(p):
    '''
    Termo : Fator
    '''
    p[0] = p[1]


def p_fator_id(p):
    'Fator : ID'
    p[0] = gerar_fator_id(p[1])


def p_fator_integer(p):
    '''
    Fator : INTEGER
    '''
    p[0] = (p[1], "integer", "")


def p_fator_real(p):
    '''
    Fator : REAL
    '''
    p[0] = (p[1], "real", "")


def p_fator_string(p):
    '''
    Fator : STRING
    '''
    p[0] = (p[1], "string", "")


def p_fator_true(p):
    '''
    Fator : TRUE
    '''
    p[0] = (1, "boolean", "")


def p_fator_false(p):
    '''
    Fator : FALSE
    '''
    p[0] = (0, "boolean", "")


def p_fator_parenthesis(p):
    '''
    Fator : '(' Expressao ')'
    '''
    p[0] = p[2]


def p_fator_array(p):
    '''
    Fator : Acesso_array
    '''
    p[0] = gerar_fator_array(p[1])


def p_fator_func_call(p):
    '''
    Fator : ChamadaFuncao
    '''
    p[0] = p[1]
