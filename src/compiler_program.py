import os
import sys
from parser.pascal_anasin import rec_Parser
from symbol_table import generalSTable


#filename = "../programas_teste/teste7.pas"
result_folder = "../programas_máquina"


def main():

    generalSTable.reset()
    print("Symbol table initialized.")

    input_path = sys.argv[1]

    if len(sys.argv) == 3:
        result_folder = sys.argv[2]

    try:
        with open(input_path, 'r') as file:
            content = file.read()

        result = rec_Parser(content)

        
        generalSTable.dump()

        
        input_filename = os.path.basename(input_path)
        output_filename = os.path.splitext(input_filename)[0] + ".out"
        os.makedirs(result_folder, exist_ok=True)
        output_path = os.path.join(result_folder, output_filename)

        
        with open(output_path, 'w') as outfile:
            outfile.write(result)

        print(f"Output written to: {output_path}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


