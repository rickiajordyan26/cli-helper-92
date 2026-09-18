import re
from typing import Any, Callable

class Rule:
    def __init__(self, check: Callable[[Any], bool], error_msg: str):
        self.check = check
        self.error_msg = error_msg

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.check(x) and other.check(x),
            f"{self.error_msg} AND {other.error_msg}"
        )

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.check(x) or other.check(x),
            f"({self.error_msg} OR {other.error_msg})"
        )

    def validate(self, value: Any) -> bool:
        if not self.check(value):
            raise ValueError(f"Validation failed for '{value}': {self.error_msg}")
        return True

def is_alphanumeric_or_dash(value: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", str(value)))

def has_min_length(length: int) -> Callable[[Any], bool]:
    return lambda x: len(str(x)) >= length

cli_arg_rule = Rule(
    lambda x: isinstance(x, str), "must be a string"
) & Rule(is_alphanumeric_or_dash, "must be alphanumeric, dash, or underscore")

port_rule = Rule(
    lambda x: str(x).isdigit(), "must be a numeric representation"
) & Rule(lambda x: 1 <= int(x) <= 65535, "must be a valid port (1-65535)")

semver_rule = Rule(
    lambda x: bool(re.match(r"^\d+\.\d+\.\d+$", str(x))),
    "must match major.minor.patch version format"
)