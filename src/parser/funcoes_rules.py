# ====== Produções de Função e Procedimento ======

def p_funcao(p):
    '''
    Dfuncao : FUNCTION ID ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN LocalInstsList END ';'
    '''
    print(f"Função reconhecida: {p[2]} com tipo de retorno {p[5]}")


def p_procedimento(p):
    '''
    Dprocedimento : PROCEDURE ID ArgumentosProcedimentoOpc ';' GlobalInsts BEGIN LocalInstsList END ';'
    '''
    print(f"Procedimento reconhecido: {p[2]}")


def p_argumentos_procedimento_opc(p):
    '''
    ArgumentosProcedimentoOpc : ArgumentosSetter
                              | 
    '''
    if len(p) == 2:
        print("Argumentos do procedimento reconhecidos")
    else:
        print("Procedimento sem argumentos")


# ====== Produções de Argumentos (Chamadas e Definições) ======

def p_argumentos_getter(p):
    '''
    ArgumentosGetter : '(' ArgumentosGetterBuffer ')'
    '''
    print("Reconhecida chamada de função com argumentos")

def p_argumentos_getter_buffer(p):
    '''
    ArgumentosGetterBuffer : ArgumentosGetterBuffer ',' Expressao
                           | Expressao
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento passado na chamada")
    elif len(p) == 2:
        print("Argumento passado na chamada")
    else:
        print("Nenhum argumento passado")

def p_argumentos_setter(p):
    '''
    ArgumentosSetter : '(' ArgumentosSetterBuffer ')'
    '''
    print("Reconhecida definição de argumentos")

def p_argumentos_setter_buffer(p):
    '''
    ArgumentosSetterBuffer : ArgumentosSetterBuffer ',' Argumento
                           | Argumento
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento declarado")
    elif len(p) == 2:
        print("Argumento declarado")
    else:
        print("Nenhum argumento declarado")

def p_argumento(p):
    '''
    Argumento : ModificadorArgumento ID ':' Tipo
    '''
    print(f"Argumento: {p[2]} com tipo {p[4]} e modificador '{p[1]}'")

def p_modificador_argumento(p):
    '''
    ModificadorArgumento : VAR
                         | CONST
                         | 
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'valor'
