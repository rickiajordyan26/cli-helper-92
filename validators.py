import re
from typing import Any, Callable, Dict, List, Optional

class InputValidator:
    """Dynamic pipeline of validator functions for CLI input."""
    def __init__(self, rules: List[Callable[[Any], bool]] = None):
        self.rules = rules or []

    def validate(self, value: Any) -> bool:
        return all(rule(value) for rule in self.rules)

    @staticmethod
    def is_non_empty(value: str) -> bool:
        return bool(value and value.strip())

    @staticmethod
    def is_email(value: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def is_within_range(min_val: int, max_val: int) -> Callable[[int], bool]:
        return lambda val: min_val <= val <= max_val

def run_checks(data: Dict[str, Any], schema: Dict[str, InputValidator]) -> Dict[str, bool]:
    return {key: schema[key].validate(data.get(key)) for key in schema}

def compose_rules(*funcs: Callable) -> List[Callable]:
    return list(funcs)

if __name__ == '__main__':
    schema = {
        'username': InputValidator([InputValidator.is_non_empty]),
        'age': InputValidator([InputValidator.is_within_range(18, 99)])
    }
    payload = {'username': 'dev_user', 'age': 25}
    results = run_checks(payload, schema)
    print(f"Validation status: {all(results.values())}")