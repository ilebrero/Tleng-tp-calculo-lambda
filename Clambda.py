#pylint: disable=C0103
"Script principal para ejecutar el parser."
from sys import argv
from lambda_parser import apply_parser

if __name__ == "__main__":
    script_input = ""
    if len(argv) > 1:
        #Uno la entrada con espacios para evitar problemas en el shell.
        script_input = " ".join(argv[1:])
    else:
        script_input = input("lambda> ")
    print(apply_parser(script_input))
