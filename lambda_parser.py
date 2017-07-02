#pylint: disable=C0103,C0111,W0611
"El parser para calculo lambda"
import ply.yacc as yacc

from operator import add, is_

from lambda_lexer import tokens
from expressions  import *

######################## Expresiones ########################

def p_true(p):
	"exp : TRUE"
	p[0] = Boolean(p[1]);

def p_false(p):
	"exp : FALSE"
	p[0] = Boolean(p[1]);

def p_if_then_else(p):
	"exp : IF exp THEN exp ELSE exp"
	p[0] = ConditionalOperation(p[2], p[4], p[6])

def p_lambda(p):
	"exp : LAMBDA VAR TYPE type POINT exp"
	p[0] = Lambda(p[2], p[4], p[6])

def p_doble_exp(p):
	"exp : exp exp"
	p[0] = BinaryExpression(p[1], p[2])

def p_num(p):
    "exp : NUMBER"
    p[0] = Number(p[1])

def p_is_zero(p):
    "exp : ISZERO L_BRACKET exp R_BRACKET"
    p[0] = BinaryNumericOperation(p[3], Number(0), is_)

def p_pred(p):
    "exp : PRED L_BRACKET exp R_BRACKET"
    p[0] = BinaryNumericOperation(p[3], Number(-1), add)

def p_succ(p):
    "exp : SUCC L_BRACKET exp R_BRACKET"
    p[0] = BinaryNumericOperation(p[3], Number(1), add)

def p_var(p):
	"exp : VAR"
	p[0] = VAR(p[1])

######################## Tipos ########################

def p_bool(p):
	"type : BOOL"
	p[0] = p[1]

def p_nat(p):
	"type : NAT"
	p[0] = p[1]

def p_lambda_type(p):
	"type : type LAMBDA_TYPE type"
	p[0] = p[3]

def p_error(_):
	print("Hubo un error en el parseo.")
	parser.restart()

# # Build the parser
# parser = yacc.yacc(debug=True)

# def apply_parser(string, tokens):
#     return parser.parse(sring, tokens)
