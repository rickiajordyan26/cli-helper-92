import time
import random
import functools
from typing import Callable, TypeVar, Any, Generator

T = TypeVar('T')


def _jittered_backoff(base: float, factor: float, limit: float) -> Generator[float, None, None]:
    current = base
    while True:
        jitter = random.uniform(0.85, 1.15)
        yield min(current * jitter, limit)
        current *= factor


def network_retry(
    max_attempts: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Decorator implementing dynamic jittered exponential backoff for functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            timeline = _jittered_backoff(base_delay, 2.0, max_delay)
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise exc
                    delay = next(timeline)
                    time.sleep(delay)
            raise RuntimeError("Execution exceeded attempt limit")
        return wrapper
    return decorator


class ResilientExecutor:
    """Dynamic runner wrapper for safe network execution on raw callables."""
    def __init__(self, **retry_options: Any):
        self.options = retry_options

    def run(self, action: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        retry_decorator = network_retry(**self.options)
        return retry_decorator(action)(*args, **kwargs)
