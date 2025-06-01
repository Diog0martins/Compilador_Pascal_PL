from symbol_table import generalSTable

def gerar_funcao(p):
    func_name = p[1]
    global_insts = p[2]
    local_insts = p[4]

    code = f"\n{func_name}:{global_insts}\n{local_insts}"
    ret_val = generalSTable.get_func_return_code(func_name)
    if ret_val:
        code += ret_val
    code += "\nRETURN\n"

    generalSTable.set_state("global")
    return code

def juntar_variaveis(p):
    return p[1] + p[2] if len(p) == 3 else "\n"

def declarar_funcao(p):
    func_name, arg_types, func_return_type = p[1], p[2], p[4]
    generalSTable.set_state("global")
    generalSTable.add_function(func_name, func_return_type, arg_types)
    generalSTable.set_state(func_name)
    return func_name

def gerar_procedimento(p):
    proc_name = p[2]
    print(f"Procedimento reconhecido: {proc_name}")
    return ""  # Completar se for necessário

def tratar_argumentos_opc(p):
    if len(p) == 2:
        print("Argumentos do procedimento reconhecidos")
        return p[1]
    else:
        print("Procedimento sem argumentos")
        return []

# ===== Argumentos =====

def tratar_argumentos_getter_init(p):
    if len(p) == 3:
        return p[1] + [p[2]]
    return []

def tratar_argumentos_getter_buffer(p):
    if len(p) == 4:
        return p[1] + [p[2]]
    return []

def configurar_argumentos_setter(p, func_name):
    generalSTable.set_state(func_name)
    argumentos = p[2]

    arg_types = []
    offset = -len([nome for _, nomes in argumentos for nome in nomes])

    for tipo, nomes in argumentos:
        for nome in nomes:
            if generalSTable.has_variable(nome):
                raise ValueError(f"Variável '{nome}' já declarada.")
            generalSTable.add_variable(nome, tipo, offset)
            offset += 1
        arg_types.extend([tipo] * len(nomes))

    return arg_types

def tratar_argumentos_setter_buffer(p):
    if len(p) == 4:
        return p[1] + [(p[3][0], p[3][1:])]
    elif len(p) == 2:
        return [(p[1][0], p[1][1:])]
    return []

def montar_argumento(p):
    nomes = p[1] + [p[2]]
    tipo = p[4].lower()
    return [tipo] + nomes

def tratar_outros_argumentos(p):
    return p[1] + [p[2]] if len(p) == 4 else []

# ===== Funções =====

def gerar_chamada_funcao(p):
    func_name = p[1]
    arguments = p[2]

    # Funções embutidas
    if func_name.lower() in ("write", "writeln"):
        return gerar_write(func_name, arguments)

    if func_name.lower() in ("read", "readln"):
        return gerar_read(func_name, arguments)

    if func_name.lower() == "length":
        return gerar_length(arguments)

    return gerar_funcao_comum(func_name, arguments)

def gerar_write(func_name, arguments):
    code = ""
    for val, tipo, inst in arguments:
        if inst:
            code += inst
        if not inst:
            if tipo == "string":
                code += f'\nPUSHS {val}\nWRITES'
            elif tipo == "integer":
                code += f'\nPUSHI {val}\nWRITEI'
            elif tipo == "real":
                code += f'\nPUSHR {val}\nWRITER'
            elif tipo == "boolean":
                code += f'\nPUSHI {1 if val == "TRUE" else 0}\nWRITEI'
        else:
            code += f"\n{inst}"
            code += f"\nWRITE{tipo[0].upper()}"

    if func_name.lower() == "writeln":
        code += "\nWRITELN"
    return code

def gerar_read(func_name, arguments):
    code = ""
    for arg in arguments:
        var_name = arg[0]
        var_type = generalSTable.get_type(var_name)
        pos = generalSTable.get_position(var_name)

        code += "READ"
        if var_type == "integer":
            code += "\nATOI"
        elif var_type == "real":
            code += "\nATOF"

        if generalSTable.is_array(var_name):
            lines = arg[2].split("\n")
            lines = [l for l in lines if "LOADN" not in l]
            code = "\n".join(lines) + "\n" + code + "\nSTOREN"
        else:
            if pos != -1:
                code += f"\nSTOREG {pos}"
            else:
                code += f"\nSTOREL {generalSTable.get_getter(var_name)}"

    if func_name.lower() == "readln":
        code += "\nWRITELN"

    return code

def gerar_length(arguments):
    var = arguments[0]
    code = '\n' + var[2] + "\nSTRLEN"
    return ("length(" + var[0] + ")", "integer", code)

def gerar_funcao_comum(func_name, arguments):
    if generalSTable.get_func_return(func_name) != "None":
        code = "\nPUSHI 0"
    else:
        code = ""

    for val, tipo, inst in arguments:
        if inst:
            code += "\n" + inst
        else:
            if tipo == "integer":
                code += f"\nPUSHI {val}"
            elif tipo == "real":
                code += f"\nPUSHF {val}"
            elif tipo == "string":
                code += f'\nPUSHS {val}'
            elif tipo == "boolean":
                code += f"\nPUSHI {1 if val else 0}"
            else:
                raise Exception(f"Tipo desconhecido: {tipo}")

    code += f"\nPUSHA {func_name}\nCALL"
    return (func_name, generalSTable.get_func_return(func_name), code)
