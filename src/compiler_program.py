from parser.pascal_anasin import rec_Parser
import sys


def main():
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
        return rec_Parser(content)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

