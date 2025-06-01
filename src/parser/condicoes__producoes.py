from codegen.condicoes import (
    gerar_condicao_logica,
    gerar_declaracao_condicao,
    traduzir_simbolo_condicional
)

# ====== Produções de Condições ======

def p_Condicao(p):
    '''
    Condicao : Condicao AND Condicao
             | Condicao OR Condicao
             | NOT Condicao
             | DeclaracaoCondicao
             | '(' Condicao ')'
    '''
    p[0] = gerar_condicao_logica(p)


def p_DeclaracaoCondicao(p):
    '''
    DeclaracaoCondicao : Expressao SimboloCondicional Expressao
                       | Expressao
    '''
    p[0] = gerar_declaracao_condicao(p)


def p_SimboloCondicional(p):
    '''
    SimboloCondicional : '='
                       | DIFFERENT
                       | LESSOREQUAL
                       | '<'
                       | GREATEROREQUAL
                       | '>'
    '''
    p[0] = traduzir_simbolo_condicional(p)
