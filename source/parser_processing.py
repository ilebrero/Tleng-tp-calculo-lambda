#pylint: disable=C0103,C0111
import re

from ply.lex import lex
from ply.yacc import yacc

import lambda_lexer
import lambda_parser
from expressions import get_type_str, Lambda
from lambda_lexer import global_context

def hack_numbers(text, result):
    "cambia los numeros por combinación de succ cuando corresponde"
    def calc_succ(match):
        i = int(match.group(0))
        res = "0"
        for _ in range(i):
            res = "succ(" + res
        res += ")"*i
        return res
    if not re.match(r".*[1-9]\d*", text):
        return re.sub(r"([1-9]\d*)", calc_succ, result)
    else:
        return result

def process_entry(text):
    lexer = lex(module=lambda_lexer)
    parser = yacc(module=lambda_parser, debug=True)

    expression = parser.parse(text, lexer)
    result = expression.evaluate()
    if isinstance(result, Lambda):
        res_type = result.type
    else:
        res_type = type(result)
    global_context.clear()
    #Hago las conversiones necesarias para mostrar bien los tipos
    if isinstance(res_type, tuple):
        a = get_type_str(res_type[0])
        b = get_type_str(res_type[1])
        if isinstance(res_type[0], tuple):
            a = "(" + a + ")"
        if isinstance(res_type[1], tuple):
            b = "(" + b + ")"
        res_type = "%s->%s" %(a, b)
    else:
        res_type = get_type_str(res_type)
    return "%s:%s" %(hack_numbers(text, str(result)), res_type)
