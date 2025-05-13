from parser.pascal_anasin import rec_Parser
import sys

import symbol_table

#filename = "../programas_teste/teste7.pas"


def main():

    symbol_table.reset()
    print("Symbol table initialized.")

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
            result = rec_Parser(content)
            symbol_table.dump()
            return result
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    

if __name__ == "__main__":
    main()

