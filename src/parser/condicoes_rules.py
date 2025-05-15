# ====== Produções de Condições ======

def p_Condicao(p):
    '''
    Condicao : Condicao AND DeclaracaoCondicao
             | Condicao OR DeclaracaoCondicao
             | NOT Condicao
             | DeclaracaoCondicao
             | '(' Condicao ')'
    '''
    if len(p) == 4:
        left = p[1]
        right = p[3]
        logic_op = p[2].upper()

        op_code = "AND" if logic_op == "AND" else "OR"
        p[0] = f"{left}\n{right}\n{op_code}"

    elif len(p) == 3:
        inner = p[2]
        p[0] = f"{inner}\nNOT"
    else:
        p[0] = p[1]



def p_DeclaracaoCondicao(p):
    '''
    DeclaracaoCondicao : Expressao SimboloCondicional Expressao
                       | Fator
    '''
    if len(p) == 4:
        left_val, left_type, left_code = p[1]
        right_val, right_type, right_code = p[3]
        op_code = p[2]

        if left_type != right_type:
            print("Erro: tipos incompatíveis na condição")
            p[0] = "; erro de tipo"
            return

        # Constant folding
        if left_val is not None and right_val is not None:
            result = eval_condition(op_code, left_val, right_val)
            p[0] = f"PUSHI {1 if result else 0}"
        else:
            # Emit PUSH for constants if no code
            left_push = left_code if left_code else f"PUSHI {left_val}" if left_type == "integer" else f"PUSHF {left_val}"
            right_push = right_code if right_code else f"PUSHI {right_val}" if right_type == "integer" else f"PUSHF {right_val}"
            p[0] = f"{left_push}\n{right_push}\n{op_code}"

    else:
        val, val_type, val_code = p[1]
        if val_type != "boolean":
            print("Erro: condição esperava valor booleano")
        if val_code:
            p[0] = val_code
        else:
            p[0] = f"PUSHI {1 if val else 0}"


def eval_condition(op, left, right):
    if op == "EQUAL":
        return left == right
    elif op == "NEQ":
        return left != right
    elif op == "INF":
        return left < right
    elif op == "INFEQ":
        return left <= right
    elif op == "SUP":
        return left > right
    elif op == "SUPEQ":
        return left >= right
    return False



def p_SimboloCondicional(p):
    '''
    SimboloCondicional : '='
                       | '<' '>'
                       | '<' '='
                       | '<'
                       | '>' '='
                       | '>'
    '''
    symbols = {
        '=': "EQUAL",
        '<>': "NEQ",
        '<=': "INFEQ",
        '<': "INF",
        '>=': "SUPEQ",
        '>': "SUP"
    }

    if len(p) == 1:
        symbol = p[1]
    else:
        symbol = p[1] + p[2]

    p[0] = symbols[symbol]
