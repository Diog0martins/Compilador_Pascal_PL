# ====== Produções Principais ======


def p_programa(p):
    '''
    Programa : PROGRAM ID ';' Duses GlobalInsts BlocoPrincipal '.'
    '''


def p_globalinsts(p):
    '''
    GlobalInsts : GlobalInsts GlobalInst
                | 
    '''

def p_globalinst(p):
    '''
    GlobalInst : Dvariaveis
            | Dfuncao
            | Dprocedimento
    '''

def p_blocofinal(p):
    '''
    BlocoPrincipal : BEGIN LocalInstsList END
    '''
