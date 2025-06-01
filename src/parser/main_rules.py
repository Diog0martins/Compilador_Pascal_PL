# ====== Produções Principais ======


def p_programa(p):
    '''
    Programa : PROGRAM ID ';' Duses GlobalInsts BlocoPrincipal '.'
    '''
    p[0] = p[5] + "\nSTART\n" + p[6] + "\nSTOP"

def p_globalinsts(p):
    '''
    GlobalInsts : GlobalInsts GlobalInst
                | 
    '''
    if len(p) == 3:
        print((p[1]))
        print((p[2]))

        p[0] = p[1] + p[2]
    else:
        p[0] = ""

def p_globalinst(p):
    '''
    GlobalInst : Dvariaveis
               | Dfuncao
               | Dprocedimento
    '''
    print(p[1])
    p[0] = p[1]
    print("Acabei de ler uma instrução global")

def p_blocofinal(p):
    '''
    BlocoPrincipal : BEGIN LocalInstsList END
    '''
    p[0] = p[2]
