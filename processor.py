import sys
import re
from typing import Callable, Any, NamedTuple


class ValidationResult(NamedTuple):
    is_valid: bool
    sanitized_value: Any
    error_message: str = ""


class Validator:
    def __init__(self, check_fn: Callable[[str], bool], error_msg: str, transform_fn: Callable[[str], Any] = str):
        self.check_fn = check_fn
        self.error_msg = error_msg
        self.transform_fn = transform_fn

    def __call__(self, value: str) -> ValidationResult:
        if self.check_fn(value):
            return ValidationResult(True, self.transform_fn(value))
        return ValidationResult(False, value, self.error_msg)

    def __or__(self, other: "Validator") -> "Validator":
        def combined_check(val: str) -> bool:
            res1 = self(val)
            return res1.is_valid and other(res1.sanitized_value).is_valid

        def combined_transform(val: str) -> Any:
            return other.transform_fn(self.transform_fn(val))

        return Validator(combined_check, f"{self.error_msg} | {other.error_msg}", combined_transform)


NON_EMPTY = Validator(lambda s: bool(s and s.strip()), "input cannot be empty", str.strip)
NO_SPECIAL_CHARS = Validator(lambda s: bool(re.match(r"^[a-zA-Z0-9_\-\s]+$", s)), "contains forbidden characters")
MAX_LENGTH = Validator(lambda s: len(s) <= 50, "exceeds length limit of 50")


def process_input_stream(stream=sys.stdin):
    validator_pipeline = NON_EMPTY | NO_SPECIAL_CHARS | MAX_LENGTH
    processed_records = []

    print("cli-helper-92 input processor ready:")
    for raw_line in iter(stream.readline, ""):
        clean_line = raw_line.rstrip("\r\n")
        if clean_line.lower() == "exit":
            break

        validation = validator_pipeline(clean_line)
        if not validation.is_valid:
            print(f"[REJECTED] {clean_line!r} -> {validation.error_message}")
            continue

        payload = validation.sanitized_value
        processed_records.append(payload)
        print(f"[ACCEPTED] {payload}")

    return processed_records


if __name__ == "__main__":
    process_input_stream()
