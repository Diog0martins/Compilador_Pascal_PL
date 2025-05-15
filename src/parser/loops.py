from loops_table import counter

"""
VERIFICAR SE É POSSÍVEL TROCAR POR BLOCO DO MAIN
"""




def p_While(p):
    '''
    While : WHILE Condicao DO LocalInstsList
    '''
    counter.inc_while()

    idx = counter.get_while()

    start_label = f"WHILE{idx}"
    end_label = f"ENDWHILE{idx}"

    condition_code = p[2] 
    body_code = p[4]
    
    p[0] = "\n".join([
        f"{start_label}:",
        condition_code,
        f"JZ {end_label}",
        body_code,
        f"JUMP {start_label}",
        f"{end_label}:"
    ])

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