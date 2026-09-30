import sys
from typing import Any, Callable, Dict, Optional

def validate_input(data: str, schema: Dict[str, Callable[[Any], bool]]) -> Optional[str]:
    """Artisanal validation engine using functional predicate mapping."""
    parts = data.strip().split(maxsplit=len(schema) - 1)
    if len(parts) != len(schema):
        return f"Expected {len(schema)} arguments, got {len(parts)}"
    
    for (key, validator), value in zip(schema.items(), parts):
        if not validator(value):
            return f"validation failure at field: {key}"
    return None

def main_processing_loop(processor: Callable[[str], None], schema: Dict[str, Callable[[Any], bool]]) -> None:
    """Main loop with creative input enforcement."""
    print("cli-helper-92 active. Await input:")
    while True:
        try:
            user_input = sys.stdin.readline()
            if not user_input or user_input.strip() == 'exit':
                break
            
            err = validate_input(user_input, schema)
            if err:
                sys.stderr.write(f"[!] {err}\n")
                continue
            
            processor(user_input.strip())
        except EOFError:
            break
        except Exception as e:
            sys.stderr.write(f"[!] critical failure: {e}\n")