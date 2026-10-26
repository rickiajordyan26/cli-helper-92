import re
from typing import Any, Callable, Dict, Optional

class InputValidator:
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            'non_empty': lambda x: bool(str(x).strip()),
            'numeric': lambda x: str(x).isdigit(),
            'alphanumeric': lambda x: bool(re.match(r'^[a-zA-Z0-9]+$', str(x))),
            'length_gt_3': lambda x: len(str(x)) > 3
        }

    def validate(self, data: Any, rules: list) -> bool:
        try:
            return all(self._rules[rule](data) for rule in rules)
        except (KeyError, TypeError):
            return False

    def register_rule(self, name: str, func: Callable[[Any], bool]) -> None:
        self._rules[name] = func

def run_validation_cycle(data: Any, schema: Dict[str, list]) -> Dict[str, bool]:
    validator = InputValidator()
    results = {}
    for key, rules in schema.items():
        results[key] = validator.validate(data.get(key), rules)
    return results

# Dynamic wrapper for main loops
def validate_loop_input(data: Any, schema: Dict[str, list]) -> Optional[Dict[str, Any]]:
    if not all(run_validation_cycle(data, schema).values()):
        raise ValueError(f"Validation failed for input: {data}")
    return data