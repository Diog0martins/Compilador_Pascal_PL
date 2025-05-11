# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList Instrucao ';'
                   | Instrucao ';'
    '''
    pass

def p_instrucao(p):
    '''
    Instrucao : Atribuicao
              | InstrucaoCondicional
    '''
    pass


# BEGIN LocalInstsList END SEMICOLON