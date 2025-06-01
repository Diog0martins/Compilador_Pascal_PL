from codegen.array import gerar_acesso_array, retornar_variavel_array
from semantic.pascal_anasem import SemanticError


def p_acesso_array(p):
    '''
    Acesso_array : Variavel_array '[' Expressao ']'
    '''
    array_name = p[1]
    index_val, index_type, index_code = p[3]

    p[0] = gerar_acesso_array(array_name, index_val, index_type, index_code)



def p_variavel_array(p):
    '''
    Variavel_array : ID
                   | Acesso_array
    '''
    p[0] = retornar_variavel_array(p[1])
