#pylint: disable=C0103,C0111,W0611
"El parser para calculo lambda"
import ply.yacc as yacc
from lexer import tokens

def p_is_zero(p):
    "exp : ISZERO L_BRACKET exp R_BRACKET"
    p[0] = (p[3] == 0)

def p_num(p):
    "exp : NUM"
    p[0] = p[1]

def p_error(_):
    print("Hubo un error en el parseo.")

    parser.restart()


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(s):
    return parser.parse(s)
