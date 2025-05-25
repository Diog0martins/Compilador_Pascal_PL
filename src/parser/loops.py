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
    CicloFor : FOR Atribuicao DirecaoFor Expressao DO Instrucao
    '''

    # print('================FORCICLEDEBUG===================')

    # Obter o contador para o ciclo
    iter = counter.get_for()
    counter.inc_for()

    # Criar labels necessárias
    start_label = f'FORSTART{iter}'
    end_label = f'FOREND{iter}'


    # Fazer setup da variavel para o limite do ciclo
    setup_variable = p[2]

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

    

    # Criar variavel para o limit
    set_limit = expr_code

    # Obter a operação de incremento
    operation = p[3]

    limit_offset = f'PUSHI 1\n{operation}'

    # Obter o corpo do ciclo
    behavior = p[6]
    
    pattern = re.compile(r'(PUSH[IFL] \d+)\n(STOREG \d+)')

    setup_variable= pattern.sub(r'\t\1\n\t\2',setup_variable)


    # Funcao join é utilizada para todos os comandos seresm acopolados
    # a um \n i.e.
    # e.g. pushi 1\ncomando\n
    p[0] = '\n'.join([

        # Atribuicao valor inicial do contador
        setup_variable,


        # Colocar o limite no topo da stack
        '\t' + set_limit,
        
        # Necessário incrementar uma vez o limite dos ciclos
        limit_offset,


        # Inicio do ciclo
        f'{start_label}:',


        # Condição do ciclo
        '\tPUSHL 0',
        f"\tPUSHG {increment_position}",
        "\tEQUAL",
        "\tNOT",
        f"\tJZ {end_label}",        


        # Corpo do ciclo
        '\t' + behavior,


        # Passo de incremento/update do contador
        f'\tPUSHG {increment_position}',
        '\tPUSHI 1',
        f'\t{operation}',
        f'\tSTOREG {increment_position}',
        f'JUMP {start_label}',


        # Fim do ciclo
        # Necessário remover limite da stack
        f'{end_label}:',
        '\tPOP 1'

    ])
    



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