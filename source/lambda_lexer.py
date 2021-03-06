#pylint: disable=C0103,C0111
"Lexer para calculo lambda con Bool y Nat"

global_context = {}

def convert(var_type):
    if var_type == "Nat":
        return int
    elif var_type == "Bool":
        return bool
    else:
        a, b = var_type.split("->")
        return (convert(a.strip()), convert(b.strip()))

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
    "POINT",
    "L_BRACKET",
    "R_BRACKET",
    "ZERO",
] + list(reserved_keywords.values())

t_LAMBDA = r"\\"
t_POINT = r"\."
t_L_BRACKET = r"\("
t_R_BRACKET = r"\)"

# Espacios y tabs
t_ignore_WHITESPACES = r"[ \t]+"

def t_ZERO(t):
    r"0"
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
    r"[a-z|A-Z]+:((Nat|Bool)->(Nat|Bool)|Nat|Bool)"
    var, var_type = t.value.split(":")
    var_type = var_type.strip()
    t.value = var
    t.var_type = convert(var_type)
    global_context[t.value] = t.var_type
    return t

def t_VAR_USAGE(t):
    r"[a-z|A-Z]+"
    t.type = reserved_keywords.get(t.value,'VAR_USAGE')
    if t.value in global_context:
        t.var_type = global_context[t.value]
    return t
