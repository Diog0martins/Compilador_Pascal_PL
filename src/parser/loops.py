from loops_table import counter

import re
"""
VERIFICAR SE É POSSÍVEL TROCAR POR BLOCO DO MAIN
"""




def p_While(p):
    '''
    While : WHILE Condicao DO Instrucao
    '''
    counter.inc_while()

    idx = counter.get_while()

    start_label = f"WHILE{idx}"
    end_label = f"ENDWHILE{idx}"

    condition_code = p[2] 
    body_code = p[4]
    print("SENAITA\n\n\n" + body_code + "\n\n\n")
    
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
    start_label = f'FORSTART{counter.get_for()}'
    end_label = f'FOREND{counter.get_for()}'
    print(start_label)
    counter.inc_for()
    setup_variable = p[2]
    print('#########################')
    print(setup_variable)
    print('#########################')


    increment_position = re.findall(r'STOREG (\d+)',setup_variable)[0]

    set_limit = f"PUSHI {p[4][0]}"

    operation = p[3]

    behavior = p[6]

    p[0] = '\n'.join([
        # atribuicao do valor do iterador
        setup_variable,
        # inicio do ciclo 
        "START",
        # definicao do limite
        set_limit,
        # rotulo de inicio
        f'{start_label}:',
        # verificacao
        "PUSHL 0",
        f"PUSHG {increment_position}",
        "EQUAL",
        "NOT",
        f"JZ {end_label}",
        # corpo
        behavior,
        # alterar iterador
        f'PUSHG {increment_position}',
        'PUSHI 1',
        operation,
        f'STOREG {increment_position}',
        f'JUMP {start_label}',
        # rotulo de fim de ciclo
        f'{end_label}:',
        # retiro da variável de limite
        'POP 1',
    ])

    # p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}"
    # print("Ciclo FOR reconhecido")

def p_direcao_for(p):
    '''
    DirecaoFor : TO
               | DOWNTO
    '''
    # print(f"Direção do FOR: {p[1]}")
    if p[1] == 'to':
        print('TOTO AFRICA')
        p[0] = 'ADD'
    if p[1] == 'downto':
        print('SINDROME DOWN')
        p[0] = 'SUB'