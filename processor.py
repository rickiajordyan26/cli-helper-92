import sys
from typing import Callable, Generator

class Rule:
    def __init__(self, predicate: Callable[[str], bool], error_msg: str):
        self.predicate = predicate
        self.error_msg = error_msg

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"{self.error_msg} & {other.error_msg}"
        )

    def validate(self, value: str) -> tuple[bool, str]:
        is_valid = self.predicate(value)
        return is_valid, "" if is_valid else self.error_msg

is_not_empty = Rule(lambda s: bool(s and s.strip()), "input cannot be empty")
is_alphanumeric = Rule(lambda s: s.strip().isalnum(), "must be alphanumeric")
is_safe_length = Rule(lambda s: 3 <= len(s.strip()) <= 30, "length must be 3-30 chars")

COMMAND_VALIDATOR = is_not_empty & is_alphanumeric & is_safe_length

def process_stream(source: Generator[str, None, None]) -> None:
    """Main processing loop using combined rule validators."""
    print("=== CLI Helper 92 Interactive Processor ===")
    print("Type 'exit' or 'quit' to terminate.")

    for raw_input in source:
        cleaned = raw_input.strip()
        if cleaned.lower() in {"exit", "quit"}:
            print("Shutting down processor.")
            break

        valid, err = COMMAND_VALIDATOR.validate(cleaned)
        if not valid:
            print(f"[REJECTED] {err}", file=sys.stderr)
            continue

        checksum = sum(ord(c) for c in cleaned) % 92
        print(f"[PROCESSED] Command: '{cleaned}' | Token-ID: #92-{checksum:02d}")

def stdin_generator() -> Generator[str, None, None]:
    while True:
        try:
            yield input("cli-helper> ")
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            return

if __name__ == "__main__":
    process_stream(stdin_generator())
