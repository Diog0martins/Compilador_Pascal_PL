class SymbolTable:

    def __init__(self,object):
        self.symbol_table = dict(object.symbol_table)
        self.current_stack_position = object.current_stack_position
        self.func_pointer = -100

    def __init__(self):
        self.symbol_table = {}
        self.current_stack_position = 0
        self.func_pointer = 0

    def add_variable(self, name, var_type):
        """Adds a variable with type, position, and optional default value."""
        if name in self.symbol_table:
            raise ValueError(f"Variable '{name}' already declared.")

        self.symbol_table[name] = {
            "type": var_type,
            "position": self.current_stack_position,
        }

        self.current_stack_position += 1
        return self.symbol_table[name]
    
    def add_function(self, name, return_type, argument_types):
        """Adds a variable with type, position, and optional default value."""
        if name in self.symbol_table:
            raise ValueError(f"Variable '{name}' already declared.")

        self.symbol_table[name] = {
            "type": "Func",
            #array de strings separadas por virgulas
            "position": self.func_pointer,
            "arguments": argument_types,
            "return": return_type,

        }
        self.func_pointer = self.func_pointer + 1

        return self.symbol_table[name]

    def get_variable(self, name):
        """Returns the variable info for a given name."""
        return self.symbol_table.get(name)
    
    def get_func_args(self,func):
        return self.symbol_table[func]["arguments"].split(',')
    
    def get_func_return(self,func):
        return self.symbol_table[func]["return"]
    
    def get_position(self, name):
        """Returns the stack position of a given variable."""
        if name not in self.symbol_table:
            raise KeyError(f"Variable '{name}' not found in symbol table.")
        return self.symbol_table[name]["position"]

    def get_type(self, name):
        """Returns the type of a given variable."""
        if name not in self.symbol_table:
            raise KeyError(f"Variable '{name}' not found in symbol table.")
        return self.symbol_table[name]["type"]

    def has_variable(self, name):
        """Checks if the variable is in the symbol table."""
        return name in self.symbol_table

    def reset(self):
        """Clears the symbol table and resets the stack position."""
        self.symbol_table.clear()
        self.current_stack_position = 0

    def dump(self):
        """Prints the current state of the symbol table (for debugging)."""
        print("=== Symbol Table ===")
        for name, info in self.symbol_table.items():
            print(f"{name}: type={info['type']}, pos={info['position']}")
        print("====================")

generalSTable = SymbolTable()