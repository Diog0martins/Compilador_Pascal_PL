# ====== Produções Principais ======


def p_programa(p):
    'Programa : PROGRAM ID SEMICOLON Duses GlobalInsts BEGIN LocalInstsList END DOT'


def p_globalinsts(p):
    '''
    GlobalInsts : GlobalInsts GlobalInst
                | 
    '''


def p_globalinst(p):
    'GlobalInst : Dvariaveis'
#              | Dfuncoes
#              | Dprocedures