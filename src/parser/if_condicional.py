# ====== Produções IF/THEN/ELSE ======

def p_instrucao_condicional(p):
    '''
    InstrucaoCondicional : IF Condicao THEN BlocoCondicional ParteElse
    '''
    print("Reconhecida instrução condicional IF-THEN[-ELSE]")

def p_bloco_condicional(p):
    '''
    BlocoCondicional : Bloco
                     | Instrucao ';'
    '''
    print("Reconhecido bloco do THEN")

def p_parte_else(p):
    '''
    ParteElse : ELSE Bloco
              | ELSE Instrucao ';'
              |
    '''
    if len(p) > 1:
        print("Reconhecido bloco ELSE")

def p_bloco(p):
    '''
    Bloco : BEGIN LocalInstsList END ';'
    '''
    pass
