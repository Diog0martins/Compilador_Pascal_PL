from symbol_table import generalSTable
from semantic.pascal_anasem import (
    verificar_variavel_existe,
    verificar_tipo_inteiro,
    verificar_variavel_e_array,
    obter_tipo_variavel,
)


def gerar_acesso_array(array_name, index_val, index_type, index_code):
    verificar_variavel_existe(array_name)

    if generalSTable.is_array(array_name):
        verificar_tipo_inteiro(index_type, contexto="índice de array")

        base_type = generalSTable.get_array_base_type(array_name)
        lower_bound = generalSTable.get_array_lower_bound(array_name)
        base_pos = generalSTable.get_position(array_name)

        access_code = index_code or f"PUSHI {index_val}"

        return (
            "array",
            base_type,
            array_name,
            f"PUSHGP\nPUSHI {base_pos}\nPADD\n{access_code}\nPUSHI {lower_bound}\nSUB"
        )

    elif obter_tipo_variavel(array_name) == "string":
        verificar_tipo_inteiro(index_type, contexto="índice de strings")
        stack_pos = generalSTable.get_position(array_name)
        access_code = (
            f"PUSHG {stack_pos}" if generalSTable.current_state == "global"
            else f"PUSHL {stack_pos}" if stack_pos != -1
            else f"PUSHL {generalSTable.get_getter(array_name)}"
        )
        return (
            array_name,
            "string",
            f"{access_code}{index_code}\nPUSHI 1\nSUB\nCHARAT"
        )

    raise Exception(f"Erro: '{array_name}' não é um array ou string.")


def retornar_variavel_array(p1):
    return p1
