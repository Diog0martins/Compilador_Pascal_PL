from codegen.funcoes import *

cool_funcy_name = ""

# ====== Produções de Função e Procedimento ======

def p_funcao(p):
    '''
    Dfuncao : FuncDec BufferVar BEGIN LocalInstsList END ';'
    '''
    p[0] = gerar_funcao(p)

def p_funky_town(p):
    '''
    BufferVar : BufferVar Dvariaveis
              |
    '''
    p[0] = juntar_variaveis(p)

def p_func_dec(p):
    '''
    FuncDec : Cabeca ArgumentosSetter ':' Tipo ';'
    '''
    p[0] = declarar_funcao(p)

def p_cabeca(p):
    '''
    Cabeca : FUNCTION ID
    '''
    global cool_funcy_name
    cool_funcy_name = p[2]
    p[0] = p[2]

def p_procedimento(p):
    '''
    Dprocedimento : PROCEDURE ID ArgumentosProcedimentoOpc ';' GlobalInsts BEGIN LocalInstsList END ';'
    '''
    p[0] = gerar_procedimento(p)

def p_argumentos_procedimento_opc(p):
    '''
    ArgumentosProcedimentoOpc : ArgumentosSetter
                              | 
    '''
    p[0] = tratar_argumentos_opc(p)

# ====== Argumentos ======

def p_argumentos_getter(p):
    '''
    ArgumentosGetter : '(' ArgumentosGetterInit ')'
    '''
    p[0] = p[2]

def p_argumentos_getter_init(p):
    '''
    ArgumentosGetterInit : ArgumentosGetterBuffer Expressao
                         |
    '''
    p[0] = tratar_argumentos_getter_init(p)

def p_argumentos_getter_buffer(p):
    '''
    ArgumentosGetterBuffer : ArgumentosGetterBuffer Expressao ','
                           |
    '''
    p[0] = tratar_argumentos_getter_buffer(p)

def p_argumentos_setter(p):
    '''
    ArgumentosSetter : '(' ArgumentosSetterBuffer ')'
    '''
    global cool_funcy_name
    p[0] = configurar_argumentos_setter(p, cool_funcy_name)

def p_argumentos_setter_buffer(p):
    '''
    ArgumentosSetterBuffer : ArgumentosSetterBuffer ',' Argumento
                           | Argumento
                           |
    '''
    p[0] = tratar_argumentos_setter_buffer(p)

def p_argumento(p):
    '''
    Argumento : OutrosArgumentos ID ':' Tipo
    '''
    p[0] = montar_argumento(p)

def p_outros_argumentos(p):
    '''
    OutrosArgumentos : OutrosArgumentos ID ','
                     |
    '''
    p[0] = tratar_outros_argumentos(p)

# ====== Chamada de Funções ======

def p_ChamadaFuncao(p):
    '''
    ChamadaFuncao : ID ArgumentosGetter
    '''
    p[0] = gerar_chamada_funcao(p)

def p_ArgumentosGetter(p):
    '''
    ArgumentosGetter : '(' ListaArgumentos ')'
                     | '(' ')'
    '''
    p[0] = p[2] if len(p) == 4 else []

def p_ListaArgumentos(p):
    '''
    ListaArgumentos : ListaArgumentos ',' Expressao
                    | Expressao
    '''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]
