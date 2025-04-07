import sys
import re
from ply import lex
tokens = (
    'ID',
    'INTEGER',
    'REAL',
    'PLUS',#+
    'MINUS',#-
    'STAR',#*
    'FORWARDDASH',#/
    'EQUAL',#=
    'LESSOREQUAL',#<=
    'LESSTHAN',#<
    'GREATEROREQUAL',#>=
    'GREATERTHAN',#>
    'OPENBRACKET',#[ 
    'CLOSEBRACKET',#]
    'DOT',#.
    'COMMA',#,
    'COLON',#:
    'SEMICOLON',#;
    'OPENPARENTHESIS',#(
    'CLOSEPARENTHESIS',#)
    'POWERTO',#^
    'AT',#@
    'OPENCURLBRACKET',#{
    'CLOSECURLBRACKET',#}
    'DOLLAR',#$
    'CARDINAL',##
    'SINGLEQUOTATION',#'
    'DOUBLEQUOTATION',#"
    'DIFFERENT',

    'STRING',
    'ONELINECOMMENTS',
    'MULTILINECOMMENTS',
    'ASSIGN',
    'KEYWORD',
    'BOOLEAN',
    'DATATYPE',
)

def t_DIFFERENT(t):
    r'\<\>'
    return t

def t_STRING(t):
    r'(?P<quote>[\'\"])[^\'\"]*?(?P=quote)'
    return t

def t_DATATYPE(t):
    r'\b(integer|real|boolean|char|string)\b'
    return t

def t_BOOLEAN(t):
    r'\b(true|false)\b'
    return t

def t_KEYWORD(t):
    r'\b(and|array|begin|case|const|div|do|downto|else|end|file|for|function|goto|if|in|label|mod|nil|not|of|or|packed|procedure|program|record|repeat|set|then|to|type|until|var|while|with)\b'
    return t

def t_ONELINECOMMENTS(t):
    r'(\{[^\}]+?\})|\/\/.*'
    return t
    
def t_MULTILINECOMMENTS(t):
    r'\(\*[^(\*\))]*?\*\)'
    return t

def t_ID(t):
    r'\b[A-Za-z](?:\w+?)?\b'
    return t

def t_LESSOREQUAL(t):
    r'\<\='
    return t

def t_LESSTHAN(t):
    r'\<'
    return t

def t_GREATEROREQUAL(t):
    r'\>\='
    return t

def t_GREATERTHAN(t):
    r'\>'
    return t


t_ASSIGN = r'\:\='
t_INTEGER =r'\b\d+\b'
t_REAL =r'\b\d+\.\d+([eE][+-]?\d+)?\b'
t_PLUS =r'\+'
t_MINUS =r'\-'
t_STAR =r'\*'
t_FORWARDDASH =r'\/'
t_EQUAL =r'\='

t_OPENBRACKET =r'\['
t_CLOSEBRACKET =r'\]'
t_DOT =r'\.'
t_COMMA =r'\,'
t_COLON =r'\:'
t_SEMICOLON =r'\;'
t_OPENPARENTHESIS =r'\('
t_CLOSEPARENTHESIS =r'\)'
t_POWERTO =r'\^'
t_AT =r'\@'
t_OPENCURLBRACKET =r'\{'
t_CLOSECURLBRACKET =r'\}'
t_DOLLAR =r'\$'
t_CARDINAL =r'\#'
t_SINGLEQUOTATION =r'\''
t_DOUBLEQUOTATION =r'\"'



t_ignore = '\t\n '


def t_error(t):
    t.lexer.skip(1)
    return "error found"

lexer = lex.lex(reflags=re.IGNORECASE)

t = """
program HelloWorld;
begin
    writeln('Ola, Mundo!');
end.
"""

if not len(sys.argv) == 1: 
    lexer.input(t)
    while r := lexer.token():
        print(r)

else:
    t = ''
    for line in sys.stdin:
        t += line
    lexer.input(t)
    while r:= lexer.token():
        print(r)