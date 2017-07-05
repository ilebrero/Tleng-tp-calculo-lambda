#pylint: disable=C0103,C0111
"Script principal para ejecutar el parser."

import sys
from parser_processing import process_entry

if __name__ == "__main__":
    script_input = ""
    if len(sys.argv) > 1:
        #Uno la entrada con espacios para evitar problemas en el shell.
        script_input = " ".join(sys.argv[1:])
    else:
        script_input = input("lambda> ")

    try:
        print(process_entry(script_input))
    except KeyError as e:
        print("ERROR: El termino no es cerrado (%s esta libre)." %(e), file=sys.stderr)
        sys.exit(1)
    except TypeError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)
