# ====== Produções de Atribuições ======

def p_atribuicao(p):
    'Atribuicao : Atribuido ASSIGN Expressao'
    print(f"Atribuição reconhecida: {p[1]} := {p[3]}")

def p_atribuido(p):
    '''
    Atribuido : ID
              | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Arrays ======

def p_acesso_array(p):
    'Acesso_array : Variavel_array OPENBRACKET Expressao CLOSEBRACKET'
    p[0] = f"{p[1]}[{p[3]}]"
    print(f"Acesso a array reconhecido: {p[0]}")

def p_variavel_array(p):
    '''
    Variavel_array : ID
                   | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Expressões ======

def p_expressao(p):
    '''
    Expressao : Expressao PLUS Termo
              | Expressao MINUS Termo
              | Termo
    '''
    if len(p) == 4:
        p[0] = f"({p[1]} {p[2]} {p[3]})"
        print(f"Expressão reconhecida: {p[0]}")
    else:
        p[0] = p[1]

def p_termo(p):
    '''
    Termo : Termo STAR Fator
          | Termo FORWARDDASH Fator
          | Fator
    '''
#          | Termo MOD Fator
    if len(p) == 4:
        p[0] = f"({p[1]} {p[2]} {p[3]})"
        print(f"Termo reconhecido: {p[0]}")
    else:
        p[0] = p[1]

def p_fator(p):
    '''
    Fator : ID
          | REAL
          | INTEGER
          | STRING
          | BOOLEAN 
          | OPENPARENTHESIS Expressao CLOSEPARENTHESIS
          | Acesso_array
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


#P.S.: RETIRAR BOOLEAN E VOLTAR A POR COND, NÃO ESQUECER 

#| ID OPENPARENTHESIS arguments CLOSEPARENTHESIS
#           | condition