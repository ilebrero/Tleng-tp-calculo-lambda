#pylint: disable=C0103,C0111,W0611
"El parser para calculo lambda"
import sys
import ply.yacc as yacc

from operator import add, is_

from lambda_lexer import tokens
from expressions  import *

######################## Expresiones ########################

precedence = [
    ('left', 'APP')
]

def p_brackets(p):
    "exp : L_BRACKET exp R_BRACKET"
    p[0] = Brackets(p[2])

def p_exp_abs(p):
    "exp : abs"
    p[0] = p[1]

def p_abs(p):
    "abs : LAMBDA dec POINT exp"
    p[0] = Lambda(p[2], p[4])

def p_abs_con(p):
    "abs : con"
    p[0] = p[1]

def p_conditional(p):
    "con : IF exp THEN exp ELSE exp"
    p[0] = ConditionalOperation(p[2], p[4], p[6])

def p_con_app(p):
    "con : app"
    p[0] = p[1]

def p_application(p):
    "app : exp exp %prec APP"
    p[0] = Application(p[1], p[2])

#def p_exp2_exp(p):
#    "exp2 : exp"
#    p[0] = p[1]

def p_app_fun(p):
    "app : fun"
    p[0] = p[1]

def p_is_zero(p):
    "fun : ISZERO L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(0), is_)

def p_pred(p):
    "fun : PRED L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(-1), add)

def p_succ(p):
    "fun : SUCC L_BRACKET exp R_BRACKET"
    p[0] = NatOperation(p[3], Number(1), add)    

def p_fun_val(p):
    "fun : val"
    p[0] = p[1]

def p_cero(p):
    "val : ZERO"
    p[0] = Number(p[1])

def p_true(p):
    "val : TRUE"
    p[0] = Boolean(p[1])

def p_false(p):
    "val : FALSE"
    p[0] = Boolean(p[1])

def p_val_var(p):
    "val : var"
    p[0] = p[1]

def p_var(p):
    "dec : VAR_DECLARATION"
    p[0] = Var(p[1])

def p_var_from_exp(p):
    "var : VAR_USAGE"
    p[0] = Var(p[1])

def p_error(_):
    print("Hubo un error en el parseo. Sintaxis invalida", file=sys.stderr)
    sys.exit(1)
