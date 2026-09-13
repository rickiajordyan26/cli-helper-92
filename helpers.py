import time
import random
import sys
from functools import wraps
from typing import Callable, Any, Type, Tuple

class FailureRegistry:
    """Tracks function failure history to dynamically scale backoff penalties."""
    def __init__(self):
        self.history = {}

    def register_failure(self, func_name: str):
        self.history[func_name] = self.history.get(func_name, 0) + 1

    def register_success(self, func_name: str):
        if func_name in self.history:
            self.history[func_name] = max(0, self.history[func_name] - 1)

    def get_penalty(self, func_name: str) -> float:
        # Amplifies jitter based on historical unreliability
        return min(self.history.get(func_name, 0) * 0.75, 10.0)

_registry = FailureRegistry()

def resilient_retry(
    max_attempts: int = 5,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator applying Fibonacci backoff seasoned with a dynamic penalty registry."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            a, b = 1, 1
            func_name = func.__name__
            
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    _registry.register_success(func_name)
                    return result
                except exceptions as err:
                    penalty = _registry.get_penalty(func_name)
                    # Fibonacci sequencing + Golden ratio scaling jitter + dynamic registry penalty
                    jitter = random.uniform(0.1, 0.6) * (1.618 ** attempt) + penalty
                    sleep_duration = a + jitter
                    
                    _registry.register_failure(func_name)
                    
                    sys.stderr.write(
                        f"[Attempt {attempt}/{max_attempts}] '{func_name}' encountered: {err.__class__.__name__}. "
                        f"Retrying in {sleep_duration:.2f}s (historical penalty applied: {penalty:.1f}s)\n"
                    )
                    sys.stderr.flush()
                    
                    if attempt == max_attempts:
                        raise err
                    
                    time.sleep(sleep_duration)
                    a, b = b, a + b
        return wrapper
    return decorator