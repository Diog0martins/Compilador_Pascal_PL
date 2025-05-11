"""
VERIFICAR SE É POSSÍVEL TROCAR POR BLOCO DO MAIN
"""


def p_While(p):
    '''
    While : WHILE Condicao DO LocalInstsList
    '''
    print (
        p[1], # Type of cycle
        p[2], # Condition
        p[4], # Block of instructions
    )



# ====== Produções do Ciclo FOR ======

def p_ciclo_for(p):
    '''
    CicloFor : FOR Atribuicao DirecaoFor Expressao DO LocalInstsList
    '''
    print("Ciclo FOR reconhecido")

def p_direcao_for(p):
    '''
    DirecaoFor : TO
               | DOWNTO
    '''
    print(f"Direção do FOR: {p[1]}")