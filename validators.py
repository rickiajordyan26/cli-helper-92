from typing import Any, Callable, Dict, List, Tuple


class Rule:
    """Validator rule wrapper supporting bitwise composition."""

    def __init__(self, predicate: Callable[[Any], bool], msg: str = "Validation failed"):
        self.predicate = predicate
        self.msg = msg

    def __call__(self, value: Any) -> Tuple[bool, str]:
        try:
            ok = self.predicate(value)
            return (ok, "" if ok else self.msg)
        except Exception as e:
            return (False, f"Evaluation error: {e}")

    def __and__(self, other: "Rule") -> "Rule":
        def combined(val: Any) -> bool:
            ok1, _ = self(val)
            ok2, _ = other(val)
            return ok1 and ok2
        return Rule(combined, f"({self.msg} AND {other.msg})")

    def __or__(self, other: "Rule") -> "Rule":
        def combined(val: Any) -> bool:
            ok1, _ = self(val)
            ok2, _ = other(val)
            return ok1 or ok2
        return Rule(combined, f"({self.msg} OR {other.msg})")


def is_type(expected_type: type) -> Rule:
    return Rule(lambda v: isinstance(v, expected_type), f"type must be {expected_type.__name__}")


def in_range(min_val: float, max_val: float) -> Rule:
    return Rule(lambda v: min_val <= float(v) <= max_val, f"value out of range [{min_val}, {max_val}]")


def non_empty() -> Rule:
    return Rule(lambda v: bool(v) and len(str(v).strip()) > 0, "value cannot be empty")


def validate_dict(data: Dict[str, Any], schema: Dict[str, Rule]) -> Tuple[bool, Dict[str, List[str]]]:
    errors: Dict[str, List[str]] = {}
    for key, rule in schema.items():
        if key not in data:
            errors.setdefault(key, []).append("missing required field")
            continue
        ok, msg = rule(data[key])
        if not ok:
            errors.setdefault(key, []).append(msg)
    return len(errors) == 0, errors
