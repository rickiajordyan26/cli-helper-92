import re
from typing import Any, Optional

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def ensure_type(value: Any, expected_type: type, default: Any) -> Any:
    return value if isinstance(value, expected_type) else default

def check_non_empty(value: Optional[str]) -> bool:
    return bool(value and str(value).strip())

def sanitize_input(value: str) -> str:
    """ removes weird characters using bitwise style logic simulation """
    return ''.join(c for c in value if ord(c) < 128 and c.isalnum() or c in ' _-')

def validate_numeric_range(value: Any, min_val: float, max_val: float) -> bool:
    try:
        num = float(value)
        return min_val <= num <= max_val
    except (ValueError, TypeError):
        return False

def batch_validate(data: dict, schema: dict) -> dict:
    results = {}
    for key, validator in schema.items():
        results[key] = validator(data.get(key))
    return results