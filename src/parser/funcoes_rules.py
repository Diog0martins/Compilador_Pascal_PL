from symbol_table import generalSTable
from symbol_table import SymbolTable

# ====== Produções de Função e Procedimento ======

def p_funcao(p):
    '''
    Dfuncao : FUNCTION ID ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN LocalInstsList ID ':' '=' Expressao ';' END ';'
            | FUNCTION ID ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN ID ':' '=' Expressao ';' END ';'

    '''
    print("==============FUNÇÃO==============")
    global generalSTable
    func_name_last = ""
    return_exp = ""

    if len(p) == 17:
        return_exp = p[13]
        func_name_last = p[10]
        local_insts = p[9]
    
    else:
        return_exp = p[12]
        func_name_last = p[9]
        local_insts = ""
    


    if p[2] != func_name_last:
        return


    l = []
    amount = 0
    argumentos = []
    generalSTable.dump()
    # [(str,[a,b,c]),(int,[d,e,f])]
    for x in p[3]:
        for i in x[1]:
            l.append(x[0])
            argumentos.append(i)
            amount += 1

    generalSTable.add_function(p[2], p[5], l)
    local_table = SymbolTable()
    local_table.current_stack_position = generalSTable.current_stack_position

    for name, x in generalSTable.symbol_table.items():
        if x["type"] == "Func":
            local_table.add_function(name, x["return"], x["arguments"])


    func_name = p[2]
    code = f"{func_name}:"
    amount *= -1


    # [(str,[a,b,c]),(int,[d,e,f])]
    for x in p[3]:
        for y in x[1]:
            code = code + f"\nPUSHFP\nLOAD {amount}"
            print(amount)
            amount = amount + 1
            if local_table.has_variable(y):
                print("AW HELL NAW!")
                return
            
            local_table.add_variable(y,x[0])
    
    prev_table = SymbolTable(generalSTable)
    generalSTable = SymbolTable(local_table)
    print("=============FRED==============")
    print(return_exp)
    print("=============FRED==============")

    code = code + p[7]
    code = code + local_insts


    """     
match(p[5]):
        case "string":
            code = code + f"\n PUSHS {return_exp}"
        case "boolean":
            if return_exp == "TRUE":
                code = code + f"\n PUSHI {1}"
            else:
                code = code + f"\n PUSHI {0}"
        case "integer":
            code = code + f"\n PUSHI {return_exp}"
        case "real":
            code = code + f"\n PUSHR {return_exp}" 
    """

    code = code + return_exp[2] +"\nRETURN\n"
    generalSTable.reset()
    generalSTable = SymbolTable(prev_table)

    p[0] = code

    
    #print(f"Função reconhecida: {p[2]} com tipo de retorno {p[5]}")

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
    ArgumentosGetter : '(' ArgumentosGetterBuffer ')'
    '''
    #print("Reconhecida chamada de função com argumentos")

    p[0] = p[2]

def p_argumentos_getter_buffer(p):
    '''
    ArgumentosGetterBuffer : ArgumentosGetterBuffer ',' Expressao
                           | Expressao
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento passado na chamada")
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        print("Argumento passado na chamada")
        p[0] = [p[1]]
    else:
        print("Nenhum argumento passado")


def p_argumentos_setter(p):
    '''
    ArgumentosSetter : '(' ArgumentosSetterBuffer ')'
    '''
    print("Reconhecida definição de argumentos")
    p[0] = p[2]

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
    
    if generalSTable.has_variable(p[2]): 
        print("AW HELL NAWH!")
        return
    
    #print(f"Argumento: {p[2]} com tipo {p[4]} e modificador '{p[1]}'")
    l = p[1] + [p[2]]

    for x in l:
        generalSTable.add_variable(x,p[4].lower())    

    p[0] = p[4]


    # [TIPO, ID1, ID2, ID3]
    p[0] = [p[0]] + l
    

def p_outros_argumentos(p):
    '''
    OutrosArgumentos : OutrosArgumentos ID ','
                     | 
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]

    else:
        p[0] = []
