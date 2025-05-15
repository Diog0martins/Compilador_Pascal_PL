from loops_table import counter

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

    counter.inc_while()

    start_label = f"WHILE{counter.get_while()}"
    end_label = f'ENDWHILE{counter.get_while()}'

    jump_cond = f'JZ {end_label}'
    jump = f'JUMP {start_label}'

    cond_1 = f'push Cond'

    cond_2 = f'push cond2'

    cond_op = f'EQUAL'

    p[0] = "\n".join([start_label + ':',cond_1,cond_2,cond_op,jump_cond,p[4],jump,end_label+':'])

    # p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"



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