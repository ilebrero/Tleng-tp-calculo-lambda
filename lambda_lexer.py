#pylint: disable=C0103,C0111
"Lexer para calculo lambda con Bool y Nat"

#Palabras reservadas
reserved_key_words = {
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'if'     : 'IF',
    'then'   : 'THEN',
    'else'   : 'ELSE',
    'succ'   : 'SUCC',
    'pred'   : 'PRED',
    'iszero' : 'ISZERO',
    'Nat'    : 'NAT',
    'Bool'   : 'BOOL'
}

#Defino los tokens
tokens = [
    "VAR",
    "LAMBDA",
    "TYPE",
    "POINT",
    "L_BRACKET",
    "R_BRACKET",
    "NUMBER",
    "LAMBDA_TYPE"
] + list(reserved_key_words.values())

t_LAMBDA = r"\\"
t_TYPE   = r":"
t_POINT  = r"\."
t_L_BRACKET = r"\("
t_R_BRACKET = r"\)"
t_LAMBDA_TYPE = r"->"

# Espacios y tabs
t_ignore_WHITESPACES = r"[ \t]+"

def t_VAR(t):
    r"[a-z|A-Z]+"
    t.type = reserved_key_words.get( t.value, 'VAR' )
    return t

def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_error(t):
    message  = "\n------------------ Illegal character ------------------"
    message += "\ntype:"  + t.type
    message += "\nvalue:" + str(t.value)
    message += "\nline:"  + str(t.lineno)
    message += "\nposition:"  + str(t.lexpos)
    message += "\n-------------------------------------------------------\n"

    print(message)
    t.lexer.skip(1)