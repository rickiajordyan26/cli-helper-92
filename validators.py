import re
from typing import Any, Callable, List, Tuple


class ValidationResult:
    def __init__(self, is_valid: bool, error: str = ""):
        self.is_valid = is_valid
        self.error = error

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        return "Valid" if self.is_valid else f"Invalid({self.error})"


class Rule:
    def __init__(self, check_fn: Callable[[Any], bool], error_message: str):
        self.check_fn = check_fn
        self.error_message = error_message

    def __call__(self, value: Any) -> ValidationResult:
        try:
            if self.check_fn(value):
                return ValidationResult(True)
            return ValidationResult(False, self.error_message)
        except Exception as e:
            return ValidationResult(False, f"Evaluation error: {e}")

    def __or__(self, other: "Rule") -> "Rule":
        def composed_check(val: Any) -> bool:
            return bool(self(val) or other(val))
        return Rule(composed_check, f"({self.error_message} OR {other.error_message})")

    def __and__(self, other: "Rule") -> "Rule":
        def composed_check(val: Any) -> bool:
            return bool(self(val) and other(val))
        return Rule(composed_check, f"({self.error_message} AND {other.error_message})")


IS_NOT_EMPTY = Rule(
    lambda v: bool(v and str(v).strip()), "value cannot be empty"
)
IS_ALPHANUMERIC = Rule(
    lambda v: str(v).isalnum(), "value must be alphanumeric"
)
IS_PATH_SAFE = Rule(
    lambda v: not re.search(r'[<>:"|?*]', str(v)),
    "value contains illegal path characters",
)

CLI_IDENTIFIER = IS_NOT_EMPTY & IS_ALPHANUMERIC
CLI_PATH = IS_NOT_EMPTY & IS_PATH_SAFE


def validate_cli_arg(arg: Any, *rules: Rule) -> Tuple[bool, List[str]]:
    errors = []
    for rule in rules:
        res = rule(arg)
        if not res:
            errors.append(res.error)
    return len(errors) == 0, errors
