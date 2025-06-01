from loops_table import counter
from codegen.ciclos import *
import re
"""
VERIFICAR SE É POSSÍVEL TROCAR POR BLOCO DO MAIN
"""




def p_While(p):
    '''
    While : WHILE Condicao DO Instrucao
    '''
    p[0] = generate_while(p[2],p[4])


# ====== Produções do Ciclo FOR ======

def p_ciclo_for(p):
    '''
    CicloFor : FOR Atribuicao DirecaoFor Expressao DO Instrucao
    '''
    p[0] = generate_for(p[2],p[3],p[4],p[6])



def p_direcao_for(p):
    '''
    DirecaoFor : TO
               | DOWNTO
    '''
    p[0] = get_for_direction(p[1])