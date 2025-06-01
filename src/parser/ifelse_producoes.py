from loops_table import counter
from codegen.condicionais import gerar_condicionais

# ====== Produções IF/THEN/ELSE ======

def p_instrucao_condicional(p):
    '''
    InstrucaoCondicional : IF Condicao THEN BlocoCondicional ParteElse
    '''
    print("Reconhecida instrução condicional IF-THEN[-ELSE]")

    p[0] = gerar_condicionais(p[2],p[4],p[5])

def p_bloco_condicional(p):
    '''
    BlocoCondicional : Instrucao
    '''
    print("Reconhecido bloco do THEN")
    p[0] = p[1]

def p_parte_else(p):
    '''
    ParteElse : ELSE Instrucao
              | 
    '''
    if len(p) > 1:
        p[0] = f"{p[1]} {p[2]}"
        print("Reconhecido bloco ELSE")
        p[0] = p[2]
    else:
        print("Não há bloco Else")
        p[0] = '\n'
