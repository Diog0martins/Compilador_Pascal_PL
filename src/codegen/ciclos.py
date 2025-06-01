from loops_table import counter
import re

def generate_while(condition_code,body_code):

    # Incrementar o contador de while
    counter.inc_while()

    # Obter o contador de while
    idx = counter.get_while()

    # Criar a label de inicio de ciclo
    start_label = f"WHILE{idx}"
    # Criar label de fim de ciclo
    end_label = f"ENDWHILE{idx}"


    return "\n".join([
        f"{start_label}:",
        condition_code,
        f"JZ {end_label}",
        body_code,
        f"JUMP {start_label}",
        f"{end_label}:"
    ])

def generate_for(iterator,dir,limit,body):
     # Obter o contador para o ciclo
    iter = counter.get_for()
    counter.inc_for()

    # Criar labels necessárias
    start_label = f'FORSTART{iter}'
    end_label = f'FOREND{iter}'


    # Fazer setup da variavel para o limite do ciclo
    setup_variable = iterator
    increment_position = re.findall(r'STOREG (\d+)',setup_variable)[0]

    expr_val, expr_type, expr_code = limit

    if expr_code == "":
        # Constant folding — no need for code execution
        if expr_type == "integer":
            expr_code = f"PUSHI {expr_val}"
        elif expr_type == "string" or expr_type == "boolean" or expr_type == "real":
            print(f"{expr_val} do tipo '{expr_type}' não é integer")
            return ""
        else:
            print(f"Tipo desconhecido '{expr_type}'")
            return ""

    

    # Criar variavel para o limit
    set_limit = expr_code

    # Obter a operação de incremento
    operation = dir

    limit_offset = f'PUSHI 1\n{operation}'

    # Obter o corpo do ciclo
    behavior = body
    
    pattern = re.compile(r'(PUSH[IFL] \d+)\n(STOREG \d+)')

    setup_variable= pattern.sub(r'\1\n\2',setup_variable)


    # Funcao join é utilizada para todos os comandos seresm acopolados
    # a um \n i.e.
    # e.g. pushi 1\ncomando\n
    return '\n'.join([

        # Atribuicao valor inicial do contador
        setup_variable,


        # Colocar o limite no topo da stack
        set_limit,
        
        # Necessário incrementar uma vez o limite dos ciclos
        limit_offset,


        # Inicio do ciclo
        f'{start_label}:',


        # Condição do ciclo
        'PUSHL 0',
        f"PUSHG {increment_position}",
        "EQUAL",
        "NOT",
        f"JZ {end_label}",        


        # Corpo do ciclo
        behavior,


        # Passo de incremento/update do contador
        f'PUSHG {increment_position}',
        'PUSHI 1',
        f'{operation}',
        f'STOREG {increment_position}',
        f'JUMP {start_label}',


        # Fim do ciclo
        # Necessário remover limite da stack
        f'{end_label}:',
        'POP 1'

    ])


def get_for_direction(dir):
    if dir == 'to':
        return 'ADD'
    if dir == 'downto':
        return 'SUB'