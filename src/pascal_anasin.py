import ply.yacc as yaac
from pascal_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

# REGRAS

def rec_Programa():
    global prox_simb
    #print("Derivando por P1: REGRA")
    #rec_term('TOKEN')
    #print("Reconheci P1: REGRA")


def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    #prox_simb = lexer.token()
    rec_Programa()
    print("Sintax Analysis finished!")