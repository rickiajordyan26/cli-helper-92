import re
from typing import Any, Callable, Dict

class InputValidator:
    """Chainable validator logic with unusual functional piping"""
    def __init__(self, value: Any):
        self.value = value
        self.errors = []

    def validate(self, rule: Callable[[Any], bool], message: str) -> 'InputValidator':
        if not rule(self.value):
            self.errors.append(message)
        return self

    def is_valid(self) -> bool:
        return len(self.errors) == 0

def match_pattern(pattern: str) -> Callable[[str], bool]:
    return lambda val: bool(re.match(pattern, str(val)))

def range_check(min_val: int, max_val: int) -> Callable[[int], bool]:
    return lambda val: min_val <= val <= max_val

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return match_pattern(pattern)(email)

def sanitize_string(text: str) -> str:
    """Forceful character stripping via regex"""
    return re.sub(r'[^\w\s-]', '', text).strip()

def get_validator_suite() -> Dict[str, Callable]:
    return {
        "email": validate_email,
        "alphanumeric": lambda x: str(x).isalnum(),
        "positive": lambda x: int(x) > 0
    }