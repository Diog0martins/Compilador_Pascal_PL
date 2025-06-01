from symbol_table import generalSTable
import re

# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ':' '=' Expressao
    '''
    destino = p[1]
    print("==================A==================")
    print(p[1])
    print(p[4])
    print("==================A==================")

    # ===============================
    # CASO: EXPRESSÃO DO TIPO strlen
    # ===============================


    if isinstance(p[4], str):
        if re.search('strlen', p[4].lower()):
            expr_code = p[4]
            if isinstance(destino, str):  # variável simples
                pos = generalSTable.get_position(destino)

                if pos != -1:
                    p[0] = expr_code + f"\nSTOREG {pos}"
                
                else:
                    x = generalSTable.get_getter(destino)

                    p[0] = expr_code + f"\nSTOREL {x}"
                
                return
            elif isinstance(destino, tuple) and destino[0] == "array":
                _, _, _, index_code = destino
                p[0] = index_code + "\n" + expr_code + "\nSTOREN"
                return

    # ===============================
    # EXPRESSÃO NORMAL
    # ===============================
    expr_val, expr_type, expr_code = p[4]


    # --------------------------------
    # CASO 1: VARIÁVEL SIMPLES
    # --------------------------------
    if isinstance(destino, str):
        var_name = destino

        if not generalSTable.has_variable(var_name):
            print(f"Erro: variável '{var_name}' não declarada.")
            p[0] = ""
            return
        
        expected_type = generalSTable.get_type(var_name)

        
        if expected_type == "Func":
            func_return = generalSTable.get_func_return(var_name)
            if func_return == expr_type:
                if generalSTable.current_state == var_name:
                    if len(generalSTable.get_func_return_code(var_name)) == 0:
                            # Constant folding

                        generalSTable.set_func_return_code(var_name,expr_code)
                        p[0] = "\n"
                        
        else:    

            if expr_type != expected_type and expected_type not in ("integer", "real"):
                print(f"Erro: tipos incompatíveis: variável '{var_name}' é '{expected_type}', expressão é '{expr_type}'")
                p[0] = ""
                return
        
            elif expr_code == "":
                # Constant folding
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
            
            pos = generalSTable.get_position(var_name)

            if pos != -1:
                p[0] = expr_code + f"\nSTOREG {pos}"

            else:
                x = generalSTable.get_getter(destino)
                p[0] = expr_code + f"\nSTOREL {x}"
            return

    # --------------------------------
    # CASO 2: ARRAY
    # destino = ("array", base_type, array_name, index_code)
    # --------------------------------
    elif isinstance(destino, tuple) and destino[0] == "array":
        _, base_type, array_name, index_code = destino

        if expr_type != base_type:
            print(f"Erro: tipo incompatível em atribuição ao array '{array_name}'")
            p[0] = ""
            return

        if expr_code == "":
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

        p[0] = index_code + "\n" + expr_code + "\nSTOREN"
        return

    else:
        print("Erro: destino de atribuição inválido")
        p[0] = ""



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
    array_name = p[1]
    index_val, index_type, index_code = p[3]

    if not generalSTable.has_variable(array_name):
        print(f"Erro: variável array '{array_name}' não declarada.")
        p[0] = (None, "error", "")
        return

    if not generalSTable.is_array(array_name):
        print(f"Erro: '{array_name}' não é um array.")
        p[0] = (None, "error", "")
        return
    
    access_code = ""

    if index_code == "":
            if index_type == "integer":
                access_code = f"PUSHI {index_val}"
            else:
                print(f"Tipo desconhecido '{index_type}'")
                p[0] = ""
                return
    else:
        access_code = index_code


    base_type = generalSTable.get_array_base_type(array_name)
    lower_bound = generalSTable.get_array_lower_bound(array_name)
    base_pos = generalSTable.get_position(array_name)

    # Código para calcular o índice real na stack: (índice - lower_bound) + base_pos
    access_code =  f"PUSHGP\nPUSHI {base_pos}\nPADD\n" + access_code + f"\nPUSHI {lower_bound}\nSUB"
    # Isto representa a instrução para LOAD/STORE
    p[0] = ("array", base_type, array_name, access_code)


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
        print("PILONA")
        p[0] = (p[1], "error", "")
    else:
        var_type = generalSTable.get_type(name)
        pos = generalSTable.get_position(name)

        if pos == -1:
            x = generalSTable.get_getter(p[1])
            p[0] = (p[1], var_type, f"\nPUSHFP\nLOAD {x}")

        else:
            p[0] = (p[1], var_type, f"\nPUSHG {pos}")
        



def p_fator_integer(p):
    '''
    Fator : INTEGER
    '''
    p[0] = (p[1], "integer", "") # Value tipo Codigo


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
    destino = p[1]

    if isinstance(destino, tuple) and destino[0] == "array":
        _, base_type, array_name, index_code = destino
        code = f"{index_code}\nLOADN"
        p[0] = (array_name, base_type, code)



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
    # print(f"Chamada de função reconhecida: {p[1]}{p[2]}")


    func_name = p[1]
    arguments = p[2]


    if func_name.lower() == "writeln" or func_name.lower() == "write":
        #generalSTable.add_function("write", "None", "string")
        #generalSTable.add_function("writeln", "None", "string")

        p[0] = ""
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

    elif func_name.lower() == "readln" or func_name.lower() == "read":
        p[0] = ""
        for arg in arguments:
            var_name = arg[0]
            var_type = generalSTable.get_type(var_name)
            var_pos = generalSTable.get_position(var_name)

            # Instruções de leitura e conversão
            p[0] += f"READ"
            match arg[1]:
                case "integer":
                    p[0] += f"\nATOI"
                case "real":
                    p[0] += f"\nATOF"

            # Verifica se é array
            if generalSTable.is_array(var_name):
                print("Sou array")
                array_name, base_type, index_code = arg

                # Remove o LOADN se estiver presente
                lines = index_code.split("\n")
                lines = [line for line in lines if "LOADN" not in line]
                cleaned_index_code = "\n".join(lines)

                # Gera o código final sem o LOADN
                p[0] = cleaned_index_code + "\n" + p[0] + "\nSTOREN"
            else:
                if var_pos != -1:
                    p[0] += f"\nSTOREG {var_pos}"
                    
                else:
                    x = generalSTable.get_getter(var_name)
                    p[0] += f"\nSTOREL {x}"
                # Variável simples


    elif func_name.lower() == "length":
        # generalSTable.add_function("length", "integer", "string")

        code = '\n' + p[2][0][2] + "\nSTRLEN"

        generalSTable.dump()

        x = "length(" + p[2][0][0] + ")"

        p[0] = (x,'integer',code)

    else:

        # if not generalSTable.has_variable(func_name):
                # print(f"A função [{func_name}] não existe")

        #expected_argument_types = generalSTable.get_func_args(func_name)
        print(func_name)
        print(arguments)
        if generalSTable.get_func_return(func_name) != "None": code = f"\nPUSHI 0"
        
        i = 0
        for x in arguments:
            val, type, code = x
            #if tipo != expected_argument_types[i]:
                # print(f"A função {func_name} esperava tipo [{expected_argument_types[i]}], recebeu [{tipo}]")
            if code == "":
                if type == "integer":
                    code += f"PUSHI {val}"
                elif type == "real":
                    code += f"PUSHF {val}"
                elif type == "string":
                    code += f'PUSHS "{val}"'
                elif type == "boolean":
                    code += f"PUSHI {1 if val else 0}"
                else:
                    print(f"Tipo desconhecido '{type}'")
                    p[0] = ""
                    return
            else:
                code += f"\n{code}"

        code
         
        code = code + '\n'.join([
            f"\nPUSHA {func_name}",
            "CALL",
        ])

        p[0] = (func_name, generalSTable.get_func_return(func_name), code)

        


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
