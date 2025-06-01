from codegen.atribuicoes import gerar_codigo_atribuicao


# ====== Produções de Atribuições ======
def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ASSIGN Expressao
    '''
    p[0] = gerar_codigo_atribuicao(p[1], p[3])


def p_atribuido(p):
    '''
    Atribuido : ID
              | Acesso_array
    '''
    p[0] = p[1]








