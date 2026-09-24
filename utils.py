import sys
import inspect
import functools
from typing import Callable, Any, Dict, Tuple

class EdgeCaseHandler:
    """Decorator and fallback runner for handling unexpected CLI inputs and exceptions."""

    def __init__(self, fallback: Any = None, auto_coerce: bool = True):
        self.fallback = fallback
        self.auto_coerce = auto_coerce

    def _coerce_args(self, func: Callable, args: Tuple, kwargs: Dict) -> Tuple[Tuple, Dict]:
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        new_args, new_kwargs = list(bound.args), dict(bound.kwargs)

        for param_name, param in sig.parameters.items():
            if param_name in new_kwargs:
                val = new_kwargs[param_name]
                if param.annotation != inspect.Parameter.empty:
                    try:
                        if not isinstance(val, param.annotation):
                            new_kwargs[param_name] = param.annotation(val)
                    except (ValueError, TypeError):
                        pass
        return tuple(new_args), new_kwargs

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError) as exc:
                if self.auto_coerce:
                    try:
                        c_args, c_kwargs = self._coerce_args(func, args, kwargs)
                        return func(*c_args, **c_kwargs)
                    except Exception:
                        pass
                if callable(self.fallback):
                    return self.fallback(exc, *args, **kwargs)
                return self.fallback
            except Exception as fatal_exc:
                sys.stderr.write(f"[cli-helper] edge case anomaly caught: {fatal_exc}\n")
                if callable(self.fallback):
                    return self.fallback(fatal_exc, *args, **kwargs)
                return self.fallback
        return wrapper

def safe_cast(value: Any, target_type: type, default: Any = None) -> Any:
    """Utility for safe casting of unpredictable string arguments."""
    try:
        if value is None:
            return default
        if target_type is bool and isinstance(value, str):
            return value.strip().lower() in ("true", "1", "yes", "y", "on")
        return target_type(value)
    except (ValueError, TypeError):
        return default