from symbol_table import SymbolTable,generalSTable

# ====== Produções de Função e Procedimento ======

def p_funcao(p):
    '''
    Dfuncao : FUNCTION ID ArgumentosSetter ':' Tipo ';' GlobalInsts BEGIN LocalInstsList ID ':' '=' Expressao ';' END ';'
    '''
    #function BinToInt(bin: string): integer;


    print("Estouaqui!?\n\n")

    if generalSTable.has_variable(p[2]): 
        print("AW HELL NAW!")
        return
    
    if p[2] != p[10]:
        print("AW HELL NAH")
        return
    

    print("\n\n\n\nHELP\n\n\n\n")



    local_table = SymbolTable()
    local_table.current_stack_position = generalSTable.current_stack_position

    for x in generalSTable.symbol_table:
        if x["type"] == "Func":
            local_table.add_function(x["name"], x["return_type"], x["argument_types"])

    func_name = p[1]
    argumentos = p[3]
    amount = len(p[3]) * (-1)
    code = f"{func_name}:"


    print(argumentos)



    for x in argumentos:
        code = code + f"\nPUSHFP\nLOAD {amount}"
        print(amount)
        amount = amount + 1
        if generalSTable.has_variable(x[1]):
            print("AW HELL NAW!")
            return
        
        generalSTable.add_variable(x[1],x[2])
        code = code + f'\nPUSHG {local_table.get_position(x[1])}',
    
    prev_table = generalSTable
    generalSTable = local_table

    code = code + p[7]
    code = code + p[9]



    print(p[5])
    print(p[5])
    print(p[5])
    print(p[5])

    match(p[5]):
        case "string":
            code = code + f"\n PUSHS {p[13]}"
        case "boolean":
            if p[13] == "TRUE":
                code = code + f"\n PUSHI {1}"
            else:
                code = code + f"\n PUSHI {0}"
        case "integer":
            code = code + f"\n PUSHI {p[13]}"
        case "real":
            code = code + f"\n PUSHR {p[13]}"

    code = code + "\nRETURN\n"

    generalSTable = prev_table

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
    print("\n\nHER242")
    p[0] = p[2]

    #print(p[0])




def p_argumentos_setter_buffer(p):
    '''
    ArgumentosSetterBuffer : ArgumentosSetterBuffer ',' Argumento
                           | Argumento
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento declarado")
        args = p[1]  # já é uma lista
        l = tuple(p[3][0],p[3][1],len(p[1]))
        args.append(l)
        p[0] = args


    elif len(p) == 2:
        p[0] = [p[1]]
        print("\n\n")
        #print(p[1])
        print("Argumento declarado x")
        p[0] = [(p[1][0],p[1][1],0)]

    else:
        print("Nenhum argumento declarado")
        p[0] = []

def p_argumento(p):
    '''
    Argumento : ModificadorArgumento ID ':' Tipo
    '''
    
    if generalSTable.has_variable(p[2]): 
        print("AW HELL NAWH!")
        return
    
    #print(f"Argumento: {p[2]} com tipo {p[4]} e modificador '{p[1]}'")
    p[0] = [p[2]]
    p[0].append(p[4])

    generalSTable.add_variable(p[2],p[4])

    

def p_modificador_argumento(p):
    '''
    ModificadorArgumento : VAR
                         | CONST
                         | 
    '''
    if len(p) == 2:
        p[0] = p[1]
