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

    expr_val, expr_type, expr_code = p[4]
    
    if expr_code == "":
        # Constant folding — no need for code execution
        if expr_type == "integer":
            expr_code = f"PUSHI {expr_val}"
        elif expr_type == "string" or expr_type == "boolean" or expr_type == "real":
            print(f"{expr_val} do tipo '{expr_type}' não é integer")
            p[0] = ""
            return
        else:
            print(f"Tipo desconhecido '{expr_type}'")
            p[0] = ""
            return
    
    
    set_limit = expr_code

    operation = p[3]

    behavior = p[6]

    pattern = re.compile(r'(PUSH[IFL] \d+)\n(STOREG \d+)')

    setup_variable= pattern.sub(r'\t\1\n\t\2',setup_variable)


    p[0] = '\n'.join([
        # atribuicao do valor do iterador
        setup_variable,
        # inicio do ciclo 
        # "START",
        # definicao do limite
        '\t' + set_limit,
        # rotulo de inicio
        f'{start_label}:',
        # verificacao
        "\tPUSHL 0",
        f"\tPUSHG {increment_position}",
        "\tEQUAL",
        "\tNOT",
        f"\tJZ {end_label}",
        # corpo
        '\t' + behavior,
        # alterar iterador
        f'\tPUSHG {increment_position}',
        '\tPUSHI 1',
        '\t'+operation,
        f'\tSTOREG {increment_position}',
        f'\tJUMP {start_label}',
        # rotulo de fim de ciclo
        f'{end_label}:',
        # retiro da variável de limite
        '\tPOP 1',
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
        p[0] = 'ADD'
    if p[1] == 'downto':
        p[0] = 'SUB'