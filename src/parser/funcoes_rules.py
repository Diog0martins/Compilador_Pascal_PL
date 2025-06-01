from symbol_table import generalSTable
from symbol_table import SymbolTable

# ====== Produções de Função e Procedimento ======

cool_funcy_name = ""

def p_funcao(p):
    '''
    Dfuncao : FuncDec BufferVar BEGIN LocalInstsList END ';'
    '''

    global generalSTable
    func_name = p[1]

    local_insts = p[4]
    global_insts = p[2]

    
    code = f"\n{func_name}:"
    code += global_insts + "\n"
    code += local_insts
    
    ret_val = generalSTable.get_func_return_code(func_name)

    if ret_val == "":
        return

    code += ret_val

    code += "\nRETURN\n"
    
    generalSTable.set_state("global")
    
    p[0] = code
    

def p_funky_town(p):
    '''
    BufferVar : BufferVar Dvariaveis
              |
    '''

    if len(p) == 3:

        p[0] = p[1] + p[2]
    else:
        p[0] = "\n"

def p_func_return(p):
    '''
    FuncReturn : ID ':' '=' Expressao ';'
    '''
    func_name = generalSTable.current_state
    if p[1] != func_name:
        raise SyntaxError(f"O nome '{p[1]}' não corresponde ao nome da função '{func_name}'")
    p[0] = (p[1], p[4])  # devolve a expressão e o código gerado

def p_func_dec(p):
    '''
    FuncDec : Cabeca ArgumentosSetter ':' Tipo ';'
    '''

    func_name = p[1]
    func_return_type = p[4]
    arg_types = p[2]
    
    generalSTable.set_state("global")
    generalSTable.add_function(func_name, func_return_type, arg_types)
    generalSTable.set_state(func_name)


    
    p[0] = p[1]





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
    print(f"Procedimento reconhecido: {p[2]}")


def p_argumentos_procedimento_opc(p):
    '''
    ArgumentosProcedimentoOpc : ArgumentosSetter
                              | 
    '''
    if len(p) == 2:
        print("Argumentos do procedimento reconhecidos")
        p[0] = p[1]

    

    else:
        print("Procedimento sem argumentos")


# ====== Produções de Argumentos (Chamadas e Definições) ======

def p_argumentos_getter(p):
    '''
    ArgumentosGetter : '(' ArgumentosGetterInit ')'
    '''
    #print("Reconhecida chamada de função com argumentos")

    p[0] = p[2]


def p_argumentos_getter_init(p):
    '''
    ArgumentosGetterInit : ArgumentosGetterBuffer Expressao
                           | 
    '''
    if len(p) == 3:
        print("Mais um argumento passado na chamada")
        p[0] = p[1] + [p[2]]
    elif len(p) == 1:
        p[0] = []
    else:
        print("Nenhum argumento passado")

def p_argumentos_getter_buffer(p):
    '''
    ArgumentosGetterBuffer : ArgumentosGetterBuffer Expressao ','
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento passado na chamada")
        p[0] = p[1] + [p[2]]
    else:
        print("Nenhum argumento passado")
        p[0] = []


def p_argumentos_setter(p):
    '''
    ArgumentosSetter : '(' ArgumentosSetterBuffer ')'
    '''

    generalSTable.set_state(cool_funcy_name)


    argumentos = p[2]

    arg_types = []
    amount = 0
    for tipo, nomes in argumentos:
        for nome in nomes:
            if generalSTable.has_variable(nome):
                raise ValueError(f"Variável '{nome}' já declarada no contexto atual.")
            amount+=1

        arg_types.extend([tipo] * len(nomes))

    amount *= -1

    for tipo, nomes in argumentos:
        for nome in nomes:
            generalSTable.add_variable(nome, tipo, amount)
            amount +=1

    p[0] = arg_types




    #print(p[0])




def p_argumentos_setter_buffer(p):
    '''
    ArgumentosSetterBuffer : ArgumentosSetterBuffer ',' Argumento
                           | Argumento
                           | 
    '''
    if len(p) == 4:
        t = (p[3][0],p[3][1:])
        p[0] = p[1] + [t]


    elif len(p) == 2:
        p[0] = [(p[1][0],p[1][1:])]

    else:
        print("Nenhum argumento declarado")
        p[0] = []

def p_argumento(p):
    '''
    Argumento : OutrosArgumentos ID ':' Tipo
    '''

    nomes = p[1] + [p[2]]
    tipo = p[4].lower()

    p[0] = [tipo] + nomes
    

def p_outros_argumentos(p):
    '''
    OutrosArgumentos : OutrosArgumentos ID ','
                     | 
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]

    else:
        p[0] = []
