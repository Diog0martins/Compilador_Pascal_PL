import ply.lex as lex
import re as r

tokens = (
    'PROGRAM',
    'BEGIN',
    'END',
    'VAR',
    'PROGRAMNAME',
    'ID',
    'TYPE',
    'FUNCTION',
    'STRING',
    'COLON',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'LPAR',
    'RPAR',
    'FOR',
    'WHILE'
)

def t_PROGRAM(t):
    r'program'
    return t

def t_PROGRAMNAME(t):
    r'program\s+(\w+)\s*;'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_VAR(t):
    r'var'
    return t

def t_FUNCTION(t):
    r'\w+(?=\()'
    return t

def t_STRING(t):
    r'\'.*?\''
    return t

#t_ID = r'\?\w+'

#t_NUMBER = r'\d+'
t_COLON = r':'
t_ID = r'\\?\w+'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_LPAR = r'\('
t_RPAR = r'\)'



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

def main():

    data = '''
program Fatorial;
var
n, i, fat: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(n);
    fat := 1;
    for i := 1 to n do
    fat := fat * i;
    writeln('Fatorial de ', n, ': ', fat);
end.
        '''

    lexer.input(data)

    for tok in lexer:
        print(tok)


if __name__ == '__main__':
        main()