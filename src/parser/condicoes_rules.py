# ====== Produções de Condições ======

def p_Condicao(p):
    '''
    Condicao : Condicao AND DeclaracaoCondicao
             | Condicao OR DeclaracaoCondicao
             | DeclaracaoCondicao
             | '(' Condicao ')'
    '''
    print("Condicao lógica reconhecida")

def p_DeclaracaoCondicao(p):
    '''
    DeclaracaoCondicao : Expressao SimboloCondicional Expressao
                       | NOT Condicao
                       | TRUE
                       | FALSE
    '''
    if len(p) == 4:
        print(f"Avaliando condição: {p[1]} {p[2]} {p[3]}")
    elif len(p) == 3:
        print(f"Negação lógica encontrada")
    else:
        print(f"Constante booleana: {p[1]}")

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
