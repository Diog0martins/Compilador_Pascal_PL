def p_dvariaveis(p):
    'Dvariaveis : VAR Listavariaveis'
    print("Declaração de variáveis encontrada")


def p_listavariaveis(p):
    '''
    Listavariaveis : Listavariaveis Variaveis COLON Tipo SEMICOLON
                   | 
    '''
    if len(p) > 1:
        print(f"Variáveis encontradas: {p[2]} do tipo {p[4]}")
    else:
        pass


def p_variaveis(p):
    '''
    Variaveis : Variaveis COMMA ID
              | ID
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]] 


def p_tipo(p):
    '''
    Tipo : DATATYPE
         | ARRAY OPENBRACKET Intervalo CLOSEBRACKET OF DATATYPE
         | ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 7:
        intervalo = p[3]
        tipo_base = p[6]
        p[0] = f"Array de {tipo_base} de [{intervalo}]"
    else:
        p[0] = p[1]


def p_intervalo(p):
    '''
    Intervalo : INTEGER DOT DOT INTEGER
    '''
    p[0] = f"{p[1]} a {p[4]}"
