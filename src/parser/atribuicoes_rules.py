import symbol_table

# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ':' '=' Expressao
    '''
    var_name = p[1]

    # Check if the variable exists
    if not symbol_table.has_variable(var_name):
        print(f"Erro: variável '{var_name}' não declarada.")
        p[0] = ""
        return

    position = symbol_table.get_position(var_name)

    # Generate the code for the expression + store result in variable
    expr_code = p[4]
    store_code = f"STOREG {position}"

    final_code = expr_code + "\n" + store_code
    p[0] = final_code

    print(f"Atribuição reconhecida: {var_name} := {p[4]}")



def p_atribuido(p):
    '''
    Atribuido : ID
              | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Arrays ======

def p_acesso_array(p):
    '''
    Acesso_array : Variavel_array '[' Expressao ']'
    '''
    p[0] = f"{p[1]}[{p[3]}]"
    print(f"Acesso a array reconhecido: {p[0]}")


def p_variavel_array(p):
    '''
    Variavel_array : ID
                   | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Expressões ======


def p_Expressao(p):
    '''
    Expressao : Expressao '+' Termo
              | Expressao '-' Termo
              | Termo
    '''
    if len(p) == 4:
        op = p[2]
        op_code = {"+" : "ADD", "-" : "SUB"}[op]
        p[0] = f"{p[1]}\n{p[3]}\n{op_code}"
    else:
        p[0] = p[1]



def p_termo(p):
    '''
    Termo : Termo '*' Fator
          | Termo MOD Fator
          | Termo DIV Fator
          | Fator
    '''
    if len(p) == 4:
        op = p[2].lower()
        op_code = {"*": "MUL", "mod": "MOD", "div": "DIV"}[op]
        p[0] = f"{p[1]}\n{p[3]}\n{op_code}"
    else:
        p[0] = p[1]



def p_fator_id(p):
    '''
    Fator : ID
    '''
    name = p[1]
    if not symbol_table.has_variable(name):
        print(f"Erro: variável '{name}' não declarada.")
        p[0] = (name, "error")
    else:
        var_type = symbol_table.get_type(name)
        p[0] = (name, var_type)


def p_fator_integer(p):
    '''
    Fator : INTEGER
    '''
    p[0] = (p[1], "integer")


def p_fator_real(p):
    '''
    Fator : REAL
    '''
    p[0] = (p[1], "real")


def p_fator_string(p):
    '''
    Fator : STRING
    '''
    p[0] = (p[1], "string")


def p_fator_true(p):
    '''
    Fator : TRUE
    '''
    p[0] = (1, "boolean")


def p_fator_false(p):
    '''
    Fator : FALSE
    '''
    p[0] = (0, "boolean")


def p_fator_parenthesis(p):
    '''
    Fator : '(' Expressao ')'
    '''
    p[0] = p[2]


def p_fator_array(p):
    '''
    Fator : Acesso_array
    '''
    p[0] = p[1] 


def p_fator_func_call(p):
    '''
    Fator : ChamadaFuncao
    '''
    p[0] = p[1]  



# ====== Produção para Chamadas de Função ======

def p_ChamadaFuncao(p):
    '''
    ChamadaFuncao : ID ArgumentosGetter
    '''
    print(f"Chamada de função reconhecida: {p[1]}(...)")
    p[0] = f"{p[1]}(...)"


def p_ArgumentosGetter(p):
    '''
    ArgumentosGetter : '(' ListaArgumentos ')'
                     | '(' ')'
    '''
    p[0] = '()' 

def p_ListaArgumentos(p):
    '''
    ListaArgumentos : Expressao
                    | ListaArgumentos ',' Expressao
    '''
