import sys
from typing import Callable, Any, List, Tuple


class EdgeCaseGuard:
    """Resilient decorator catching standard and bizarre CLI execution edge cases."""

    def __init__(self, default_return: Any = None, verbose: bool = False):
        self.default_return = default_return
        self.verbose = verbose
        self.fallbacks: List[Tuple[type, Callable[[BaseException], Any]]] = []

    def register_fallback(self, exc_type: type, recovery_fn: Callable[[BaseException], Any]) -> "EdgeCaseGuard":
        self.fallbacks.append((exc_type, recovery_fn))
        return self

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                clean_args = [
                    a.replace("\x00", "") if isinstance(a, str) else a
                    for a in args
                ]
                return func(*clean_args, **kwargs)
            except (KeyboardInterrupt, SystemExit):
                raise
            except BaseException as exc:
                for exc_type, handler in self.fallbacks:
                    if isinstance(exc, exc_type):
                        return handler(exc)
                if self.verbose:
                    sys.stderr.write(f"[CLI Guard] Handled edge case: {type(exc).__name__} -> {exc}\n")
                return self.default_return

        return wrapper


def safe_cli_runner(
    action: Callable[..., Any],
    *args: Any,
    fallback_value: Any = "ERR_FALLBACK"
) -> Any:
    """Executes CLI actions with standard mitigations for stdout truncation and input noise."""
    guard = EdgeCaseGuard(default_return=fallback_value, verbose=True)
    guard.register_fallback(BrokenPipeError, lambda e: sys.exit(0))
    guard.register_fallback(MemoryError, lambda e: "CLI_RESOURCE_EXHAUSTED")
    guard.register_fallback(UnicodeError, lambda e: "CLEAN_STRING_DECODE_FAILED")

    wrapped = guard(action)
    return wrapped(*args)
