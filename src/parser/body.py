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
              | CicloFor
              | InstrucaoCondicional
              | Atribuicao 
              | Expressao
    '''
    print("Acabei de ler um instrucao")


def p_instrucao_bloco(p):
     '''
     Instrucao : Bloco
     '''
     print(p[1])


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END
    '''
    p[0] = (p[1],p[3])

