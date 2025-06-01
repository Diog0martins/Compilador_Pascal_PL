# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList ';' Instrucao
    '''
    print("HELLO")
    
    p[0] = p[1] + "\n" + p[3]


def p_localinstslist_terminada(p):
    '''
    LocalInstsList : LocalInstsList ';'
    '''
    print("HELLO1")
    p[0] = p[1]

def p_localinstslist_single(p):
    '''
    LocalInstsList : Instrucao
    '''
    print("HELLO2")
    p[0] = p[1]


def p_instrucao(p):
    '''
    Instrucao : While
              | CicloFor
              | InstrucaoCondicional
              | Atribuicao 
              | Expressao
    '''
    print("HELLO3")
    p[0] = p[1]
    print("Acabei de ler um instrucao")


def p_instrucao_bloco(p):
     '''
     Instrucao : Bloco
     '''
     print("HELLO4")
     p[0] = p[1]
     print(p[1])


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END 
    '''
    print("HELLO5")
    p[0] = p[2]

