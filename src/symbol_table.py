
symbol_table = {}

current_stack_position = 0


def add_variable(name, var_type):
    """Adds a variable with type, position, and optional default value."""
    global current_stack_position

    if name in symbol_table:
        raise ValueError(f"Variable '{name}' already declared.")

    symbol_table[name] = {
        "type": var_type,
        "position": current_stack_position,
    }

    current_stack_position += 1
    return symbol_table[name]


def get_variable(name):
    """Returns the variable info for a given name."""
    return symbol_table.get(name)

def get_position(name):
    """Returns the stack position of a given variable.

    Raises an error if the variable is not found.
    """
    if name not in symbol_table:
        raise KeyError(f"Variable '{name}' not found in symbol table.")
    return symbol_table[name]["position"]

def get_type(name):
    """Returns the type of a given variable.

    Raises an error if the variable is not found.
    """
    if name not in symbol_table:
        raise KeyError(f"Variable '{name}' not found in symbol table.")
    return symbol_table[name]["type"]


def has_variable(name):
    """Checks if the variable is in the symbol table."""
    return name in symbol_table


def reset():
    """Clears the symbol table and resets the stack position."""
    global current_stack_position
    symbol_table.clear()
    current_stack_position = 0


def dump():
    """Prints the current state of the symbol table (for debugging)."""
    print("=== Symbol Table ===")
    for name, info in symbol_table.items():
        print(f"{name}: type={info['type']}, pos={info['position']}")
    print("====================")
