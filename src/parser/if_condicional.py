# ====== Produções IF/THEN/ELSE ======

def p_instrucao_condicional(p):
    '''
    InstrucaoCondicional : IF Condicao THEN BlocoCondicional ParteElse
    '''
    print("Reconhecida instrução condicional IF-THEN[-ELSE]")
    p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}{p[5]}"

def p_bloco_condicional(p):
    '''
    BlocoCondicional : LocalInstsList
    '''
    print("Reconhecido bloco do THEN")
    p[0] = f"{p[1]} "

def p_parte_else(p):
    '''
    ParteElse : ELSE LocalInstsList
              | 
    '''
    if len(p) > 1:
        p[0] = f"{p[1]} {p[2]}"
        print("Reconhecido bloco ELSE")

    else:
        print("Não há bloco Else")
