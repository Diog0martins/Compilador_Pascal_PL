# ====== Produções do corpo do programa ======

def p_localinstslist_multiple(p):
    '''
    LocalInstsList : LocalInstsList ';' Instrucao
    '''
    print("Instruções acumuladas")

    p[0] = f"{p[1]} {p[2]} {p[3]}"



def p_localinstslist_terminada(p):
    '''
    LocalInstsList : LocalInstsList ';'
    '''
    print("Final com ponto e vírgula opcional")

    p[0] = f"{p[1]} {p[2]}"



def p_localinstslist_single(p):
    '''
    LocalInstsList : Instrucao
    '''
    print("Instrução única")
    p[0] = p[1]


def p_instrucao(p):
    '''
    Instrucao : While
              | CicloFor
              | InstrucaoCondicional
              | Atribuicao 
              | Expressao
    '''

    p[0] = p[1]
    print("Acabei de ler um instrucao")


def p_instrucao_bloco(p):
     '''
     Instrucao : Bloco
     '''
     p[0] = p[1]
     print(p[1])


def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END
    '''
    p[0] = f"{p[1]} {p[2]} {p[3]}"

