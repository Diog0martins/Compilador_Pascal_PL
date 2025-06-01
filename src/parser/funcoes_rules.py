from symbol_table import generalSTable
from symbol_table import SymbolTable

# ====== Produções de Função e Procedimento ======

cool_funcy_name = ""

def p_funcao(p):
    '''
    Dfuncao : Cabeca ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN LocalInstsList ID ':' '=' Expressao ';' END ';'
            | Cabeca ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN ID ':' '=' Expressao ';' END ';'

    '''
    print("==============FUNÇÃO==============")
    print(p[8])
    print("==============FUNÇÃO==============")
    global generalSTable
    func_name = p[1]
    global cool_funcy_name
    cool_funcy_name = func_name
    func_return_type = p[4]
    arg_types = p[2]

    if len(p) == 17:
        return_exp = p[12]
        final_name = p[9]
        local_insts = p[8]
        global_insts = p[6]
        
    else:
        return_exp = p[11]
        final_name = p[8]
        local_insts = ""
        global_insts = p[6]
    
    print(return_exp)

    if func_name != final_name:
        return
    print("1")

    generalSTable.add_function(func_name, func_return_type, arg_types)

    code = f"{func_name}:"




    code += global_insts
    code += local_insts
    code += return_exp[2]
    code += "\nRETURN\n"
    
    generalSTable.set_state("global")
    
    p[0] = code

    
    #print(f"Função reconhecida: {p[2]} com tipo de retorno {p[5]}")

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
        p[1].append(p[2])
        p[0] = p[1]
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
    print("Reconhecida definição de argumentos")
    print(p[2])

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
