from symbol_table import generalSTable
from semantic.pascal_anasem import (
    verificar_variavel_existe,
    verificar_tipos_iguais,
    verificar_atribuicao_tipo,
    SemanticError,
)


def gerar_codigo_atribuicao(destino, expressao):
    if isinstance(expressao, str) and 'strlen' in expressao.lower():
        return _gerar_atribuicao_strlen(destino, expressao)

    expr_val, expr_type, expr_code = expressao

    if isinstance(destino, str):
        return _gerar_atribuicao_variavel(destino, expr_val, expr_type, expr_code)

    elif isinstance(destino, tuple) and destino[0] == "array":
        return _gerar_atribuicao_array(destino, expr_val, expr_type, expr_code)

    else:
        raise SemanticError("Erro: destino de atribuição inválido")


def _gerar_atribuicao_strlen(destino, expr_code):
    verificar_variavel_existe(destino)

    if isinstance(destino, str):  # variável simples
        pos = generalSTable.get_position(destino)
        if pos != -1:
            return expr_code + f"\nSTOREG {pos}"
        else:
            x = generalSTable.get_getter(destino)
            return expr_code + f"\nSTOREL {x}"
    elif isinstance(destino, tuple) and destino[0] == "array":
        _, _, _, index_code = destino
        return index_code + "\n" + expr_code + "\nSTOREN"
    raise SemanticError("Erro: destino inválido para strlen")


def _gerar_atribuicao_variavel(var_name, expr_val, expr_type, expr_code):
    verificar_variavel_existe(var_name)

    expected_type = generalSTable.get_type(var_name)

    # Atribuição ao nome da função (retorno)
    if expected_type == "Func":
        func_return = generalSTable.get_func_return(var_name)
        if func_return == expr_type and generalSTable.current_state == var_name:
            if not generalSTable.get_func_return_code(var_name):
                generalSTable.set_func_return_code(var_name, expr_code)
            return "\n"
        raise SemanticError(f"Erro: retorno da função '{var_name}' com tipo incorreto.")

    verificar_atribuicao_tipo(var_name, expr_type)

    if expr_code == "":
        expr_code = _const_folding(expr_type, expr_val)

    pos = generalSTable.get_position(var_name)
    if pos != -1:
        return expr_code + f"\nSTOREG {pos}"
    else:
        x = generalSTable.get_getter(var_name)
        return expr_code + f"\nSTOREL {x}"


def _gerar_atribuicao_array(destino, expr_val, expr_type, expr_code):
    _, base_type, array_name, index_code = destino
    verificar_tipos_iguais(expr_type, base_type, contexto=f"atribuição ao array '{array_name}'")

    if expr_code == "":
        expr_code = _const_folding(expr_type, expr_val)

    return index_code + "\n" + expr_code + "\nSTOREN"


def _const_folding(tipo, valor):
    if tipo == "integer":
        return f"\nPUSHI {valor}"
    elif tipo == "real":
        return f"\nPUSHF {valor}"
    elif tipo == "string":
        return f'\nPUSHS "{valor}"'
    elif tipo == "boolean":
        return f"\nPUSHI {1 if valor else 0}"
    else:
        raise SemanticError(f"Erro: tipo desconhecido '{tipo}'")
