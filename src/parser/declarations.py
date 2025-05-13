def p_dvariaveis(p):
    'Dvariaveis : VAR Listavariaveis'
    print("Declaração de variáveis encontrada")


def p_listavariaveis(p):
    '''
    Listavariaveis : Listavariaveis Variaveis ':' Tipo ';'
                   | 
    '''
    if len(p) > 1:
        print(f"Variáveis encontradas: {p[2]} do tipo {p[4]}")
    else:
        pass


def p_variaveis(p):
    '''
    Variaveis : Variaveis ',' ID
              | ID
    '''
    if len(p) == 4:
        p[0] = f"{p[1]},{p[3]}"
    else:
        p[0] = p[1] 


def p_tipo(p):
    '''
    Tipo : Datatype
         | ARRAY '[' Intervalo ']' OF Datatype
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
    Intervalo : INTEGER '.' '.' INTEGER
    '''
    p[0] = f"{p[1]} a {p[4]}"


def p_datatype(p):
    '''
    Datatype : REAL_TYPE
             | INTEGER_TYPE
             | STRING_TYPE
             | BOOLEAN_TYPE
             | CHAR_TYPE
    '''
    p[0] = p[1]