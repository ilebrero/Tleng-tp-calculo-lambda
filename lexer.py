#pylint: disable=C0103,C0111
"Lexer para calculo lambda con Bool y Nat"

from ply import lex

#Defino los tokens
tokens = (
    "VAR",
    "TRUE",
    "FALSE",
    "IF",
    "THEN",
    "ELSE",
    "LAMBDA",
    "TYPE",
    "POINT",
    "SUCC",
    "L_BRACKET",
    "R_BRACKET",
    "PRED",
    "ISZERO",
    "BOOL",
    "NAT",
    "NUM"
)

t_VAR = r"[a-z]"
t_TRUE = r"true"
t_FALSE = r"false"
t_IF = r"if"
t_THEN = r"then"
t_ELSE = r"else"
t_LAMBDA = r"\\"
t_TYPE = r":"
t_POINT = r"\."
t_SUCC = r"succ"
t_L_BRACKET = r"\("
t_R_BRACKET = r"\)"
t_PRED = r"pred"
t_ISZERO = r"iszero"
t_BOOL = r"Bool"
t_NAT = r"Nat"

def t_NUM(t):
    r"\d+"
    t.value = int(t.value)
    return t

t_ignore = " \t\n"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Construyo el lexer

lexer = lex.lex()

def apply_lexer(string):
    "Aplica el lexer al string dado"
    lexer.input(string)
    return list(lexer)
