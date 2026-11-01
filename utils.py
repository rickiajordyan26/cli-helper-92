import random
import time
import urllib.error
import urllib.request
from functools import wraps
from typing import Any, Callable, Generator, Tuple, Type, Union


def _fibonacci_jitter_stream(base: float = 0.5, max_delay: float = 10.0) -> Generator[float, None, None]:
    """Yields backoff delays combining Fibonacci sequence with chaotic jitter."""
    a, b = base, base
    while True:
        jitter = random.uniform(0.8, 1.3)
        current_delay = min(a * jitter, max_delay)
        yield current_delay
        a, b = b, a + b


def network_retry(
    max_attempts: int = 5,
    catch_exceptions: Tuple[Type[BaseException], ...] = (OSError, TimeoutError, urllib.error.URLError),
    backoff_base: float = 0.2,
) -> Callable:
    """Decorator applying fibonacci-jittered retry logic to volatile network operations."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = _fibonacci_jitter_stream(base=backoff_base)
            last_err: Union[BaseException, None] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    delay = next(delays)
                    time.sleep(delay)

            if last_err:
                raise last_err
        return wrapper
    return decorator


@network_retry(max_attempts=3)
def fetch_remote_payload(url: str, timeout: float = 5.0) -> bytes:
    req = urllib.request.Request(url, headers={'User-Agent': 'cli-helper-92/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()
