import re
from typing import Any, Callable, List, Tuple


class Rule:
    def __init__(self, func: Callable[[Any], bool], msg: str = "Invalid value"):
        self.func = func
        self.msg = msg

    def __call__(self, value: Any) -> Tuple[bool, str]:
        valid = bool(self.func(value))
        return valid, ("" if valid else self.msg)

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda v: self(v)[0] or other(v)[0],
            f"({self.msg} OR {other.msg})",
        )

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda v: self(v)[0] and other(v)[0],
            f"({self.msg} AND {other.msg})",
        )


class ValidatorPipeline:
    def __init__(self, **rules: Rule):
        self._rules = rules

    def validate(self, **data: Any) -> Tuple[bool, List[str]]:
        errors = []
        for key, rule in self._rules.items():
            if key not in data:
                errors.append(f"Missing required field: '{key}'")
                continue
            ok, err = rule(data[key])
            if not ok:
                errors.append(f"Field '{key}': {err}")
        return len(errors) == 0, errors


is_str = Rule(lambda x: isinstance(x, str), "Must be a string")
is_int = Rule(lambda x: isinstance(x, int) and not isinstance(x, bool), "Must be an integer")
non_empty = Rule(lambda x: len(str(x).strip()) > 0, "Cannot be empty string")
is_email = Rule(lambda x: bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", str(x))), "Must be a valid email")
is_positive = Rule(lambda x: isinstance(x, (int, float)) and x > 0, "Must be positive")

cli_input_validator = ValidatorPipeline(
    username=is_str & non_empty,
    email=is_str & is_email,
    age=is_int & is_positive,
)