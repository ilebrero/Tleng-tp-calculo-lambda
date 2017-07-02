#pylint: disable=C0103
"Script principal para ejecutar el parser."

import lambda_lexer
import lambda_parser

from sys import argv

from ply.lex import lex
from ply.yacc import yacc

#TODO: 
# 1) Agregar Vals -> V ::== true | false | \x:T.M | n
# 1') suc^n()?
# 2) Matchear diferencia de tipos (expressions?)
# 3) Hacer eval de LAMBDA
# 4) Ver la parte de checkeo de typos

def process_entry(text):
	lexer  = lex(module=lambda_lexer)
	parser = yacc(module=lambda_parser, debug=True)

	expression = parser.parse(text, lexer)

	print(expression.evaluate())

if __name__ == "__main__":
    script_input = ""
    if len(argv) > 1:
        #Uno la entrada con espacios para evitar problemas en el shell.
        script_input = " ".join(argv[1:])
    else:
        script_input = input("lambda> ")

    process_entry(script_input)