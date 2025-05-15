import symbol_table

# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ':' '=' Expressao
    '''
    var_name = p[1]
    if not symbol_table.has_variable(var_name):
        print(f"Erro: variável '{var_name}' não declarada.")
        p[0] = ""
        return

    expected_type = symbol_table.get_type(var_name)
    expr_val, expr_type, expr_code = p[4]

    if expr_type != expected_type:
        print(f"Erro: tipos incompatíveis: variável '{var_name}' é '{expected_type}', expressão é '{expr_type}'")
        p[0] = ""
        return

    if expr_val is not None:
        # Constant folding — no need for code execution
        if expr_type == "integer":
            expr_code = f"PUSHI {expr_val}"
        elif expr_type == "real":
            expr_code = f"PUSHF {expr_val}"
        elif expr_type == "string":
            expr_code = f'PUSHS "{expr_val}"'
        elif expr_type == "boolean":
            expr_code = f"PUSHI {1 if expr_val else 0}"
        else:
            print(f"Tipo desconhecido '{expr_type}'")
            p[0] = ""
            return

    pos = symbol_table.get_position(var_name)
    p[0] = expr_code + f"\nSTOREG {pos}"

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

def p_Expressao_complex(p):
    '''
    Expressao : Expressao '+' Termo
              | Expressao '-' Termo
    '''
    left_val, left_type, left_code = p[1]
    right_val, right_type, right_code = p[3]
    op = p[2]

    if left_type != right_type:
        print("Erro: tipos incompatíveis na expressão")
        p[0] = (None, "error", "")
        return

    op_code = "ADD" if op == '+' else "SUB"

    # ===== Constant folding =====
    if left_val is not None and right_val is not None:
        result = left_val + right_val if op == '+' else left_val - right_val
        p[0] = (result, left_type, "")
    else:
        left_push = left_code if left_code else f"PUSHI {left_val}" if left_type == "integer" else f"PUSHF {left_val}"
        right_push = right_code if right_code else f"PUSHI {right_val}" if right_type == "integer" else f"PUSHF {right_val}"

        code = f"{left_push}\n{right_push}\n{op_code}"
        p[0] = (None, left_type, code)


def p_Expressao(p):
    '''
    Expressao : Termo
    '''
    p[0] = p[1]



def p_termo_complex(p):
    '''
    Termo : Termo '*' Fator
          | Termo MOD Fator
          | Termo DIV Fator
    '''
    left_val, left_type, left_code = p[1]
    right_val, right_type, right_code = p[3]
    op = p[2].lower()

    if left_type != right_type:
        print("Erro: tipos incompatíveis no termo")
        p[0] = (None, "error", "")
        return

    op_map = {"*": "MUL", "mod": "MOD", "div": "DIV"}
    op_code = op_map[op]

    # ===== Constant folding =====
    if left_val is not None and right_val is not None:
        if op == "*":
            result = left_val * right_val
        elif op == "mod":
            result = left_val % right_val
        elif op == "div":
            result = left_val // right_val
        p[0] = (result, left_type, "")
    else:
        # Emit code for known values
        left_push = left_code if left_code else f"PUSHI {left_val}" if left_type == "integer" else f"PUSHF {left_val}"
        right_push = right_code if right_code else f"PUSHI {right_val}" if right_type == "integer" else f"PUSHF {right_val}"

        code = f"{left_push}\n{right_push}\n{op_code}"
        p[0] = (None, left_type, code)


def p_termo_simple(p):
    '''
    Termo : Fator
    '''
    p[0] = p[1]




def p_fator_id(p):
    'Fator : ID'
    name = p[1]
    if not symbol_table.has_variable(name):
        print(f"Erro: variável '{name}' não declarada.")
        p[0] = (None, "error", "")
    else:
        var_type = symbol_table.get_type(name)
        pos = symbol_table.get_position(name)
        p[0] = (None, var_type, f"PUSHG {pos}")



def p_fator_integer(p):
    '''
    Fator : INTEGER
    '''
    p[0] = (p[1], "integer", "")


def p_fator_real(p):
    '''
    Fator : REAL
    '''
    p[0] = (p[1], "real", "")


def p_fator_string(p):
    '''
    Fator : STRING
    '''
    p[0] = (p[1], "string", "")


def p_fator_true(p):
    '''
    Fator : TRUE
    '''
    p[0] = (1, "boolean", "")


def p_fator_false(p):
    '''
    Fator : FALSE
    '''
    p[0] = (0, "boolean", "")


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
