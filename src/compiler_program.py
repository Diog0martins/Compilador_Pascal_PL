import os
import sys
from parser.pascal_anasin import rec_Parser
import symbol_table


#filename = "../programas_teste/teste7.pas"
result_folder = "../programas_máquina"


def main():

    symbol_table.reset()
    print("Symbol table initialized.")

    input_path = sys.argv[1]

    try:
        with open(input_path, 'r') as file:
            content = file.read()

        result = rec_Parser(content)

        
        symbol_table.dump()

        
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


