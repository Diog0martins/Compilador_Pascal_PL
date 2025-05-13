# ====== Produções de Condições ======

def p_Condicao(p):
    '''
    Condicao : Condicao AND DeclaracaoCondicao
             | Condicao OR DeclaracaoCondicao
             | NOT Condicao
             | DeclaracaoCondicao
             | '(' Condicao ')'
    '''

    if len(p) == 4:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    elif len(p) == 3:
        p[0] = f"{p[1]} {p[2]}"
    else:
        p[0] = p[1]
    print(f"Condicao lógica reconhecida: {p[0]}\n")


def p_DeclaracaoCondicao(p):
    '''
    DeclaracaoCondicao : Expressao SimboloCondicional Expressao
                       | Fator
    '''
    if len(p) == 4:
        print(f"Avaliando condição: {p[1]} {p[2]} {p[3]}")
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    else:
        print(f"Constante booleana: {p[1]}")
        p[0] = p[1]


def p_SimboloCondicional(p):
    '''
    SimboloCondicional : '='
                       | '<' '>'
                       | '<' '='
                       | '<'
                       | '>' '='
                       | '>'
    '''
    p[0] = p[1]