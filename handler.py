import sys

def validate_input(data):
    checks = {
        'non_empty': lambda x: len(x.strip()) > 0,
        'no_special': lambda x: x.isalnum(),
        'length_limit': lambda x: len(x) <= 20
    }
    for name, rule in checks.items():
        if not rule(data):
            raise ValueError(f"input validation failed: {name}")
    return True

def process_main_loop():
    print("cli-helper-92 ready. type 'quit' to exit.")
    while True:
        try:
            user_input = input(">> ").strip()
            if user_input.lower() == 'quit':
                break
            
            if validate_input(user_input):
                print(f"processing verified input: {user_input.upper()}")
                
        except (ValueError, EOFError) as e:
            print(f"error: {e}. try again.")
        except Exception:
            print("fatal system anomaly")
            sys.exit(1)

if __name__ == "__main__":
    process_main_loop()