# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ':' '=' Expressao
    '''
    print(f"Atribuição reconhecida: {p[1]} := {p[4]}")

def p_atribuido(p):
    '''
    Atribuido : ID
              | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Arrays ======

def p_acesso_array(p):
    '''
    Acesso_array : Variavel_array '[' Expressao ']'
    '''
    p[0] = f"{p[1]}[{p[3]}]"
    print(f"Acesso a array reconhecido: {p[0]}")

def p_variavel_array(p):
    '''
    Variavel_array : ID
                   | Acesso_array
    '''
    p[0] = p[1]


# ====== Produções de Expressões ======

def p_Expressao(p):
    '''
    Expressao : Expressao '+' Termo
              | Expressao '-' Termo
              | Termo
    '''
    if len(p) == 4:
        p[0] = f"({p[1]} {p[2]} {p[3]})"
        print(f"Expressão reconhecida: {p[0]}")
    else:
        p[0] = p[1]

def p_termo(p):
    '''
    Termo : Termo '*' Fator
          | Termo MOD Fator
          | Termo DIV Fator
          | Fator
    '''
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
          | TRUE
          | FALSE
          | '(' Expressao ')'
          | Acesso_array
          | ChamadaFuncao
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


# ====== Produção para Chamadas de Função ======

def p_ChamadaFuncao(p):
    '''
    ChamadaFuncao : ID ArgumentosGetter
    '''
    print(f"Chamada de função reconhecida: {p[1]}(...)")
    p[0] = f"{p[1]}(...)"

# Exemplo genérico da função ArgumentosGetter
def p_ArgumentosGetter(p):
    '''
    ArgumentosGetter : '(' ListaArgumentos ')'
                     | '(' ')'
    '''
    p[0] = '()'  # Podes adaptar isto conforme necessário

def p_ListaArgumentos(p):
    '''
    ListaArgumentos : Expressao
                    | ListaArgumentos ',' Expressao
    '''
    # Implementar conforme necessário
