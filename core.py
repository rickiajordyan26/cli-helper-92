import sys
import functools
from typing import Callable, Any

class EdgeCaseRegistry:
    def __init__(self):
        self.handlers = {}

    def register(self, exc_type: Exception):
        def decorator(func: Callable):
            self.handlers[exc_type] = func
            return func
        return decorator

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = self.handlers.get(type(e))
            if handler:
                return handler(e)
            raise e

def robust_execution(registry: EdgeCaseRegistry):
    def wrapper(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return registry.execute(func, *args, **kwargs)
        return inner
    return wrapper

registry = EdgeCaseRegistry()

@registry.register(ValueError)
def handle_value_error(e):
    print(f"Caught intentional chaos: {e}")
    return None

@robust_execution(registry)
def risky_operation(data):
    if not data:
        raise ValueError("Empty input detected")
    return data.upper()