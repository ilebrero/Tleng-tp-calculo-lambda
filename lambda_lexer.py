#pylint: disable=C0103,C0111
"Lexer para calculo lambda con Bool y Nat"

global_context = {}

#Palabras reservadas
reserved_keywords = {
    'if'     : 'IF',
    'then'   : 'THEN',
    'else'   : 'ELSE',
    'succ'   : 'SUCC',
    'pred'   : 'PRED',
    'iszero' : 'ISZERO',
    'true'   : 'TRUE',
    'false'  : 'FALSE'
}

#Defino los tokens
tokens = [
    "VAR_DECLARATION",
    "VAR_USAGE",
    "LAMBDA",
    "TYPE",
    "POINT",
    "L_BRACKET",
    "R_BRACKET",
    "NUMBER",
    "LAMBDA_TYPE",
] + list(reserved_keywords.values())

t_LAMBDA = r"\\"
t_POINT = r"\."
t_L_BRACKET = r"\("
t_R_BRACKET = r"\)"
t_LAMBDA_TYPE = r"->"

# Espacios y tabs
t_ignore_WHITESPACES = r"[ \t]+"

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

def t_VAR_DECLARATION(t):
    r"[a-z|A-Z]:(Nat|Bool|(Nat|Bool)->(Nat|Bool))"
    var, var_type = t.value.split(":")
    var_type = var_type.strip()
    t.value = var
    if var_type == "Nat":
        t.var_type = int
    elif var_type == "Bool":
        t.var_type = bool
    else:
        a,b = var_type.split("->")
        t.var_type = (a.trim(), b.trim())
    global_context[t.value] = t.var_type
    return t

def t_VAR_USAGE(t):
    r"[a-z|A-Z]+"
    t.type = reserved_keywords.get(t.value,'VAR_USAGE')
    if t.value in global_context:
        t.var_type = global_context[t.value]
    return t
