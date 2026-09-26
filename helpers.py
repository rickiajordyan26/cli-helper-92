import random
import time
from functools import wraps
from typing import Callable, Any, Iterable, Type, Tuple, Optional


def golden_jitter_backoff(max_seconds: float = 8.0) -> Iterable[float]:
    """Generates golden-ratio scaled delay intervals with random jitter."""
    phi = 1.61803398875
    current = 0.2
    while True:
        yield random.uniform(0.1, min(current, max_seconds))
        current *= phi


def retry_network_op(
    max_attempts: int = 4,
    catch_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_retry: Optional[Callable[[BaseException, int, float], None]] = None
):
    """Decorator applying golden-ratio backoff retry mechanics to network calls."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = iter(golden_jitter_backoff())
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as error:
                    if attempt == max_attempts:
                        raise error
                    delay = next(delays)
                    if on_retry:
                        on_retry(error, attempt, delay)
                    time.sleep(delay)
        return wrapper
    return decorator
