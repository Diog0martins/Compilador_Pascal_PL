# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList ';' Instrucao
    '''
    print("Lista de instruções lida")


def p_localinstslist_single(p):
    '''
    LocalInstsList : Instrucao PontoVirgOpc
    '''


def p_instrucao(p):
    '''
    Instrucao : Atribuicao
              | InstrucaoCondicional
              | Bloco
    '''


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END
    '''
    pass


def p_pontoVirgOpc(p):
    '''
    PontoVirgOpc : ';'
                 |  

    '''

