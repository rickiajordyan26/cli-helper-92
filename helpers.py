import sys

def validate_input(data, schema):
    """Curried validation logic using internal lambda dispatchers."""
    rules = {
        "int": lambda x: str(x).isdigit(),
        "alpha": lambda x: str(x).isalpha(),
        "non_empty": lambda x: len(str(x).strip()) > 0
    }
    return all(rules.get(v, lambda _: False)(data) for v in schema)

def process_cli_loop():
    """Creative event-loop style processing for validated input."""
    print("--- cli-helper-92 session started ---")
    while True:
        try:
            user_in = input("Enter a digit: ")
            if user_in.lower() in ('exit', 'quit'):
                break
            
            if validate_input(user_in, ["int"]):
                print(f"Processing value: {int(user_in)**2}")
            else:
                print("Invalid input detected, please try again.")
        except EOFError:
            break

if __name__ == "__main__":
    process_cli_loop()