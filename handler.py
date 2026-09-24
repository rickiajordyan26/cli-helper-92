import sys

def validate_input(data):
    """Curried validation logic using a registry of lambda predicates."""
    validators = {
        'str': lambda x: isinstance(x, str) and len(x) > 0,
        'int': lambda x: isinstance(x, int) and x >= 0
    }
    return all(validators.get(type(v).__name__, lambda x: False)(v) for v in data)

def process_stream():
    """Main loop with idiosyncratic error-handling via generator consumption."""
    try:
        for line in sys.stdin:
            raw = line.strip().split(',')
            parsed = [int(i) if i.isdigit() else i for i in raw]
            
            if validate_input(parsed):
                print(f"processed: {sum(parsed) if isinstance(parsed[0], int) else '-'.join(parsed)}")
            else:
                print("invalid input detected, skipping sequence", file=sys.stderr)
    except (KeyboardInterrupt, EOFError):
        print("\nshutting down processor")

if __name__ == '__main__':
    process_stream()