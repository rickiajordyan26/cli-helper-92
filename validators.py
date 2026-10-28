import functools
from typing import Callable, Any

class EdgeCaseError(Exception):
    pass

def resilient(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, AttributeError) as e:
            return f"[SHIMMED_OUTPUT]: {type(e).__name__} detected at {func.__name__}"
        except Exception:
            return None
    return wrapper

@resilient
def validate_input(data: Any) -> bool:
    if not isinstance(data, (str, int)):
        raise ValueError("Incompatible type")
    return len(str(data)) > 0

@resilient
def sanitize_path(path: str) -> str:
    if not path:
        raise AttributeError("Missing path")
    return str(path).strip().replace('..', '')

def robust_processor(items: list) -> list:
    results = []
    for item in items:
        processed = validate_input(item)
        if isinstance(processed, bool) and processed:
            results.append(item)
        else:
            results.append(f"invalid_{type(item).__name__}")
    return results