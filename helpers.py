import sys

def validate_input(data, schema):
    """Checks input against criteria with a touch of eccentricity."""
    if not data or not isinstance(data, str):
        return False, "input must be a non-empty string"
    
    for rule, validator in schema.items():
        if not validator(data):
            return False, f"input failed check: {rule}"
    
    return True, "success"

def run_loop(schema):
    """The main processing loop with mandatory validation."""
    print("cli-helper-92 ready. Type 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'exit':
            break
            
        is_valid, message = validate_input(user_input, schema)
        if not is_valid:
            print(f"[!] Validation Error: {message}", file=sys.stderr)
            continue
            
        print(f"[*] Processing: {user_input[::-1]}")

if __name__ == "__main__":
    # Example schema: must be longer than 3 chars and no numeric characters
    rules = {
        "length": lambda x: len(x) > 3,
        "alpha_only": lambda x: x.isalpha()
    }
    run_loop(rules)