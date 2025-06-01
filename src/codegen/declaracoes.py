from symbol_table import generalSTable
from semantic.pascal_anasem import (
    verificar_tipo_suportado,
    verificar_intervalo_valido,
)


def declarar_variaveis_simples(lista_nomes, tipo):
    tipo = tipo.lower()
    verificar_tipo_suportado(tipo)

    if tipo == "integer" or tipo == "boolean":
        code = "PUSHI 0"
    elif tipo == "string":
        code = 'PUSHS ""'
    elif tipo == "real":
        code = "PUSHF 0"
    else:
        code = f"; tipo não reconhecido: {tipo}"

    declaracoes = []

    for nome in lista_nomes:
        generalSTable.add_variable(nome, tipo)
        declaracoes.append(code)

    return declaracoes


def declarar_arrays(lista_nomes, base_type, lower, upper):
    verificar_intervalo_valido(lower, upper)
    declaracoes = []

    size = upper - lower + 1
    for nome in lista_nomes:
        generalSTable.add_array(nome, base_type, lower, upper)
        declaracoes.append(f"PUSHN {size}")

    return declaracoes
