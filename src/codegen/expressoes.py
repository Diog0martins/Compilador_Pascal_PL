from symbol_table import generalSTable
from .atribuicoes import _const_folding
from semantic.pascal_anasem import (
    verificar_tipos_iguais,
    verificar_variavel_existe,
)


def gerar_expressao_binaria(left, op, right):
    left_val, left_type, left_code = left
    right_val, right_type, right_code = right

    verificar_tipos_iguais(left_type, right_type, contexto="operação aritmética")

    op_code = "ADD" if op == '+' else "SUB"

    if left_code == "" and right_code == "":
        result = left_val + right_val if op == '+' else left_val - right_val
        return (result, left_type, "")
    else:
        left_push = left_code or _const_folding(left_type, left_val)
        right_push = right_code or _const_folding(right_type, right_val)
        return (None, left_type, f"{left_push}\n{right_push}\n{op_code}")


def gerar_termo_binario(left, op, right):
    left_val, left_type, left_code = left
    right_val, right_type, right_code = right
    op = op.lower()

    verificar_tipos_iguais(left_type, right_type, contexto="termo aritmético")

    op_map = {"*": "MUL", "mod": "MOD", "div": "DIV"}
    op_code = op_map[op]

    if left_code == "" and right_code == "":
        if op == "*":
            result = left_val * right_val
        elif op == "mod":
            result = left_val % right_val
        elif op == "div":
            result = left_val // right_val
        return (result, left_type, "")
    else:
        left_push = left_code or _const_folding(left_type, left_val)
        right_push = right_code or _const_folding(right_type, right_val)
        return (None, left_type, f"{left_push}\n{right_push}\n{op_code}")


def gerar_fator_id(name):
    verificar_variavel_existe(name)

    var_type = generalSTable.get_type(name)
    pos = generalSTable.get_position(name)

    if pos == -1:
        x = generalSTable.get_getter(name)
        return (name, var_type, f"\nPUSHFP\nLOAD {x}")
    else:
        return (name, var_type, f"\nPUSHG {pos}")


def gerar_fator_array(destino):
    if isinstance(destino, tuple) and destino[0] == "array":
        _, base_type, array_name, index_code = destino
        return (array_name, base_type, f"{index_code}\nLOADN")
    return destino
