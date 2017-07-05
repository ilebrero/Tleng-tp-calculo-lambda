#pylint: disable=C0103,C0111,W0611
"El parser para calculo lambda"
import sys
import ply.yacc as yacc

from operator import add, is_

from lambda_lexer import tokens
from expressions  import *

######################## Expresiones ########################

def p_brackets(p):
    "exp : L_BRACKET exp R_BRACKET"
    p[0] = p[2]

def p_true(p):
    "exp : TRUE"
    p[0] = Boolean(p[1])

def p_false(p):
    "exp : FALSE"
    p[0] = Boolean(p[1])

def p_if_then_else(p):
    "exp : IF exp THEN exp ELSE exp"
    p[0] = ConditionalOperation(p[2], p[4], p[6])

def p_lambda(p):
    "exp : LAMBDA var POINT exp"
    p[0] = Lambda(p[2], p[4])

def p_apply(p):
    "exp : exp exp"
    p[0] = Application(p[1], p[2])

def p_apply_2(p):
    "exp : L_BRACKET exp R_BRACKET exp"
    p[0] = Application(p[2], p[4])

def p_num(p):
    "exp : NUMBER"
    p[0] = Number(p[1])

def p_is_zero(p):
    "exp : ISZERO L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(0), is_)

def p_pred(p):
    "exp : PRED L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(-1), add)

def p_succ(p):
    "exp : SUCC L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(1), add)

def p_var(p):
    "var : VAR_DECLARATION"
    p[0] = Var(p[1])

def p_var_from_exp(p):
    "exp : VAR_USAGE"
    p[0] = Var(p[1])

def p_error(_):
    print("Hubo un error en el parseo. Sintaxis invalida", file=sys.stderr)
    sys.exit(1)
    #parser.restart()
