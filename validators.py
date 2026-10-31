from typing import Any, Callable, Dict, List, Tuple

class Rule:
    """A composable validation rule using bitwise operators."""
    def __init__(self, predicate: Callable[[Any], bool], description: str = ""):
        self.predicate = predicate
        self.description = description or getattr(predicate, '__name__', 'custom_check')

    def __call__(self, value: Any) -> bool:
        try:
            return bool(self.predicate(value))
        except Exception:
            return False

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(lambda x: self(x) and other(x), f"({self.description} AND {other.description})")

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(lambda x: self(x) or other(x), f"({self.description} OR {other.description})")

    def __invert__(self) -> "Rule":
        return Rule(lambda x: not self(x), f"NOT({self.description})")


is_string = Rule(lambda x: isinstance(x, str), "is_str")
is_int = Rule(lambda x: isinstance(x, int) and not isinstance(x, bool), "is_int")
is_positive = Rule(lambda x: isinstance(x, (int, float)) and x > 0, "is_positive")
is_non_empty = Rule(lambda x: hasattr(x, '__len__') and len(x) > 0, "is_non_empty")

valid_identifier = is_string & is_non_empty
valid_port = is_int & is_positive & Rule(lambda x: x <= 65535, "is_valid_port")


def validate_payload(data: Dict[str, Any], schema: Dict[str, Rule]) -> Tuple[bool, List[str]]:
    """Validates dictionary structure against composed rule schema."""
    if not isinstance(data, dict):
        return False, ["Payload must be a dictionary"]
    
    errors = []
    for key, rule in schema.items():
        if key not in data:
            errors.append(f"Missing required field: '{key}'")
        elif not rule(data[key]):
            errors.append(f"Field '{key}' failed validation: {rule.description}")
            
    return len(errors) == 0, errors
