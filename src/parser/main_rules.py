# ====== Produções Principais ======


def p_programa(p):
    '''
    Programa : Cabecalho Dvariaveis Corpo DOT
             | Cabecalho Corpo
    '''
    if len(p) == 5:
        print("Cabeçalho, Declaração de Variáveis e Corpo encontrado")
    else:
        print("Cabeçalho e Corpo encontrado")


def p_cabecalho(p):
    'Cabecalho : PROGRAM Programname SEMICOLON'
    print(f"Program name: {p[2]}")


def p_programname(p):
    'Programname : ID'
    p[0] = p[1]

