# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList ';' Instrucao
    '''
    print("Instruções acumuladas")


def p_localinstslist_terminada(p):
    '''
    LocalInstsList : LocalInstsList ';'
    '''
    print("Final com ponto e vírgula opcional")


def p_localinstslist_single(p):
    '''
    LocalInstsList : Instrucao
    '''
    print("Instrução única")


def p_instrucao(p):
    '''
    Instrucao : While
              | InstrucaoCondicional
              | Bloco
              | Atribuicao 
              | Expressao
    '''
    print("Acabei de ler um instrucao")


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END
    '''
    pass


