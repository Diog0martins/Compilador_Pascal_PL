from .atribuicoes import _const_folding
from semantic.pascal_anasem import (
    verificar_tipos_iguais,
    verificar_tipo_booleano,
)


def gerar_condicao_logica(p):
    if len(p) == 4:
        if p[2].upper() in ("AND", "OR"):
            left = p[1]
            right = p[3]
            op_code = p[2].upper()
            return f"{left}\n{right}\n{op_code}"
        else:
            # Caso de parêntesis: ( Condicao )
            return p[2]
    elif len(p) == 3:
        # NOT Condicao
        return f"{p[2]}\nNOT"
    else:
        # Condicao única
        return p[1]


def gerar_declaracao_condicao(p):
    if len(p) == 4:
        left_val, left_type, left_code = p[1]
        right_val, right_type, right_code = p[3]
        op_code = p[2]

        verificar_tipos_iguais(left_type, right_type, contexto="condição")

        if left_code == "" and right_code == "":
            result = eval_condition(op_code, left_val, right_val)
            return f"PUSHI {1 if result else 0}"

        left_push = left_code or _const_folding(left_type, left_val)
        right_push = right_code or _const_folding(right_type, right_val)

        return f"{left_push}\n{right_push}\n{op_code}"

    else:
        val, val_type, val_code = p[1]
        verificar_tipo_booleano(val_type)
        return val_code or f"PUSHI {1 if val else 0}"


def eval_condition(op, left, right):
    match op:
        case "EQUAL": return left == right
        case "NEQ": return left != right
        case "INF": return left < right
        case "INFEQ": return left <= right
        case "SUP": return left > right
        case "SUPEQ": return left >= right
    return False


def traduzir_simbolo_condicional(p):
    symbols = {
        '=': "EQUAL",
        '<>': "NEQ",
        '<=': "INFEQ",
        '<': "INF",
        '>=': "SUPEQ",
        '>': "SUP"
    }

    if len(p) == 2:
        symbol = p[1]
    else:
        symbol = p[1] + p[2]  # Caso de operadores compostos (ex: '<=')

    return symbols.get(symbol, "; erro simbolo desconhecido")
