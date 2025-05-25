from symbol_table import generalSTable

# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ':' '=' Expressao
    '''
    var_name = p[1]
    # print(p[4])
    # print("==========")
    if not generalSTable.has_variable(var_name):
        # print(f"Erro: variável '{var_name}' não declarada.")
        p[0] = ""
        return

    expected_type = generalSTable.get_type(var_name)
    expr_val, expr_type, expr_code = p[4]


    if expr_type != "integer" and expr_type != "real" and expr_type != expected_type:
        # print(f"Erro: tipos incompatíveis: variável '{var_name}' é '{expected_type}', expressão é '{expr_type}'")
        p[0] = ""
        return

    if expr_code == "":
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
            # print(f"Tipo desconhecido '{expr_type}'")
            p[0] = ""
            return

    pos = generalSTable.get_position(var_name)
    p[0] = expr_code + f"\nSTOREG {pos}"

    # print(f"Atribuição reconhecida: {var_name} := {p[4]}")



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
        # print("Erro: tipos incompatíveis na expressão")
        p[0] = (None, "error", "")
        return

    op_code = "ADD" if op == '+' else "SUB"

    # ===== Constant folding =====
    if left_code == "" and right_code == "":
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
        # print("Erro: tipos incompatíveis no termo")
        p[0] = (None, "error", "")
        return

    op_map = {"*": "MUL", "mod": "MOD", "div": "DIV"}
    op_code = op_map[op]

    # ===== Constant folding =====
    if left_code == "" and right_code == "":
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
    if not generalSTable.has_variable(name):
        # print(f"Erro: variável '{name}' não declarada.")
        p[0] = (p[1], "error", "")
    else:
        var_type = generalSTable.get_type(name)
        pos = generalSTable.get_position(name)

        p[0] = (p[1], var_type, f"PUSHG {pos}")



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
    # print('É uma chamadinha de funcao')



# ====== Produção para Chamadas de Função ======

def p_ChamadaFuncao(p):
    '''
    ChamadaFuncao : ID ArgumentosGetter
    '''
    # print(f"Chamada de função reconhecida: {p[1]}{p[2]}")


    func_name = p[1].lower()
    arguments = p[2]


    if func_name == "writeln" or func_name == "write":
        #generalSTable.add_function("write", "None", "string")
        #generalSTable.add_function("writeln", "None", "string")

        p[0] = ""
        # print(p[1])
        # print(p[2])
        for x in arguments:
            if x[2] != "":
                p[0] = p[0] + x[2]
                match(x[1]):
                    case "string":
                        p[0] = p[0] + (f"\nWRITES")
                    case "integer":
                        p[0] = p[0] + (f"\nWRITEI")
                    case "real":
                        p[0] = p[0] + (f"\nWRITER")
                    case "boolean":
                        if x[0] == "TRUE":
                            p[0] = p[0] + (f"\nWRITEI")
                        else:
                            p[0] = p[0] + (f"\nWRITEI")

            else:
                match(x[1]):
                    case "string":
                        p[0] = p[0] + (f"PUSHS \"{x[0][1:-1]}\"")
                        p[0] = p[0] + (f"\nWRITES")
                    case "integer":
                        p[0] = p[0] + (f"PUSHI {x[0]}")
                        p[0] = p[0] + (f"\nWRITEI")
                    case "real":
                        p[0] = p[0] + (f"PUSHR {x[0]}")
                        p[0] = p[0] + (f"\nWRITER")
                    case "boolean":
                        if x[0] == "TRUE":
                            p[0] = p[0] + (f"PUSHI 1")
                            p[0] = p[0] + (f"\nWRITEI")
                        else:
                            p[0] = p[0] + (f"PUSHI 0")
                            p[0] = p[0] + (f"\nWRITEI")
                p[0] = p[0] + "\nWRITELN"

    elif func_name == "readln" or func_name == "read":
        p[0] = ""
        for arg in arguments:
            var_name = arg[0]

            var_type = generalSTable.get_type(var_name)
            var_pos = generalSTable.get_position(var_name)

            p[0] += f"READ"

            match var_type:
                case "integer":
                    p[0] += f"\nATOI"
                case "real":
                    p[0] += f"\nATOF"


            # Guardar valor na variável
            p[0] += f"\nSTOREG {var_pos}"


    elif func_name == "length":
        # print("\n\n")
        
        generalSTable.add_function("length", "integer", "string")
        print(p[2][0])

        code = f"\n{p[2][0][2]}" + "\nSTRLEN"

        generalSTable.dump()

        p[0] = code

        # print(p[0])

        #if p[2][0][2] == "":
        #    p[0] = f"PUSHI 1"

    else:

        # if not generalSTable.has_variable(func_name):
                # print(f"A função [{func_name}] não existe")

        expected_argument_types = generalSTable.get_func_args(func_name)

        if generalSTable.get_func_return(func_name) != "None": code = f"\nPUSHI 0"
        
        i = 0
        for x in arguments:
            tipo, code = x[1], x[2]
            # if tipo != expected_argument_types[i]:
                # print(f"A função {func_name} esperava tipo [{expected_argument_types[i]}], recebeu [{tipo}]")

            code += f"\n{code}"
            
        p[0] = p[0] + '\n'.join([
            f"PUSHA {func_name}",
            "CALL",
        ])

        p[0] = code


def p_ArgumentosGetter(p):
    '''
    ArgumentosGetter : '(' ListaArgumentos ')'
                     | '(' ')'
    '''

    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_ListaArgumentos(p):
    '''
    ListaArgumentos : ListaArgumentos ',' Expressao
                    | Expressao
    '''

    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[1].append(p[3])
        p[0] = p[1]

    # Implementar conforme necessário
