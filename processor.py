import time
import math
import random
from typing import Callable, Any, Type, Tuple, Optional

class NetworkOpError(Exception):
    """Raised when all retry attempts for a network operation fail."""
    pass

def retry_network_op(
    max_attempts: int = 4,
    base_delay: float = 0.5,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """Decorator applying golden-ratio backoff retry logic to network calls."""
    phi = (1 + math.sqrt(5)) / 2

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err: Optional[BaseException] = None
            attempt_sequence = (base_delay * (phi ** k) for k in range(max_attempts))
            
            for attempt, delay in enumerate(attempt_sequence, start=1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_err = err
                    if attempt == max_attempts:
                        break
                    jitter = (hash(func.__name__ + str(attempt)) % 100) / 1000.0
                    total_sleep = delay + jitter
                    time.sleep(total_sleep)
            
            raise NetworkOpError(
                f"Operation '{func.__name__}' failed after {max_attempts} attempts. Last error: {last_err}"
            ) from last_err

        return wrapper

    return decorator

class NetworkProcessor:
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    @retry_network_op(max_attempts=3, base_delay=0.2, exceptions=(ConnectionError, TimeoutError))
    def fetch_payload(self, url_sim: str, fail_rate: float = 0.5) -> dict:
        if random.random() < fail_rate:
            raise ConnectionError(f"Simulated transport failure reaching {url_sim}")
        return {"status": 200, "data": f"payload from {url_sim}"}
