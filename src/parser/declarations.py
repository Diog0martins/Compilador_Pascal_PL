import symbol_table

def p_dvariaveis(p):
    'Dvariaveis : VAR Listavariaveis'
    print("Declaração de variáveis encontrada")
    p[0] = p[2]


def p_listavariaveis(p):
    '''
    Listavariaveis : Listavariaveis Variaveis ':' Tipo ';'
                   | 
    '''
    if len(p) > 1:
        tipo = p[4].lower()

        if tipo == "integer":
            code = "PUSHI 0"
            default = 0
        elif tipo == "string":
            code = 'PUSHS ""'
            default = ""
        elif tipo == "real":
            code = "PUSHF 0"
            default = 0.0
        else:
            code = f"; tipo não reconhecido: {tipo}"
            default = None  

        declarations = []

        for var_name in p[2]:
            try:
                symbol_table.add_variable(var_name, tipo)
                declarations.append(code)
            except ValueError as e:
                print(f"Erro: {e}")

        joined_code = "\n".join(declarations)
        p[0] = p[1] + "\n" + joined_code if p[1] else joined_code

        print(f"Variáveis declaradas: {p[2]} do tipo {tipo}")
    else:
        p[0] = ""


def p_variaveis(p):
    '''
    Variaveis : Variaveis ',' ID
              | ID
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]] 


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