#pylint: disable=C0103
"Script principal para ejecutar el parser."
from sys import argv
from lambda_lexer import apply_lexer
#from lambda_parser import apply_parser

if __name__ == "__main__":
    script_input = ""
    if len(argv) > 1:
        #Uno la entrada con espacios para evitar problemas en el shell.
        script_input = " ".join(argv[1:])
    else:
        script_input = input("lambda> ")

    lexer = apply_lexer(script_input)    

    #Ver resultado de tokens
    for t in lexer:
    	print(t)

    #Ver resultado de pertenencia y AST
    #print(apply_parser(script_input))