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
        p[3], # Condition
        p[4], # Block of instructions
    )

    p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"



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