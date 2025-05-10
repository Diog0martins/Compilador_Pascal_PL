# ====== Produções da zona de uses/imports ======


def p_duses(p):
    '''
    Duses : USES UseList SEMICOLON
          | 
    '''

def p_uselist(p):
    '''
    UseList : UseList COMMA ID
            | ID 
    '''