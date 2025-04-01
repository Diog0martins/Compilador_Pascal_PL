from ply import lex


# Define token types with regex patterns
tokens = (
    "KEYWORD",
    "IDENTIFIER",
    "INTEGER",
    "REAL",
    "STRING",
    "OPERATOR",
    "COMPARISON",
    "ASSIGNMENT",
    "DELIMITER",
    "BRACKET",
    "COMMENT",
)

def t_KEYWORD(t):
    r"\b(program|begin|end|var|procedure|function|if|then|else|while|do|for|to|repeat|until|case|of|const|type|array|record)\b"
    return t
def t_IDENTIFIER(t):
    r"[A-Za-z][A-Za-z0-9_]*"
    return t
def t_INTEGER(t):
    r"\b\d+\b"
    return t
def t_REAL(t):
    r"\b\d+\.\d+([eE][+-]?\d+)?\b"
    return t
def t_STRING(t):
    r"'([^']*)'"
    return t
def t_OPERATOR(t):
    r"(\+|-|\*|\/|div|mod|and|or|not)"
    return t
def t_COMPARISON(t):
    r"(=|<>|<|>|<=|>=)"
    return t
def t_ASSIGNMENT(t):
    r":="
    return t
def t_DELIMITER(t):
    r"[;,\.]"
    return t
def t_BRACKET(t):
    r"[\(\)\[\]\{\}]"
    return t
def t_COMMENT(t):
    r"\{.*?\}|\(\*.*?\*\)"
    return t


t_ignore = ' '


def t_error(t):
    t.lexer.skip(1)
    return "error found"

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)
# Example Pascal code
pascal_code = """
program Test;
var x, y: integer;
begin
    x := 10;
    y := x + 20;
    writeln('Result: ', y);
end.
"""

lexer = lex.lex()

lexer.input(pascal_code)

while r := lexer.token():
    print(r)
