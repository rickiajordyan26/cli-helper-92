import time
import functools
from typing import Callable, Any

def retry(attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == attempts:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @retry(attempts=3, delay=0.5)
    def fetch_data(self, endpoint: str) -> dict:
        # simulating volatile network operations
        import random
        if random.random() < 0.7:
            raise ConnectionError('fickle network response')
        return {'status': 'success', 'data': endpoint}

if __name__ == '__main__':
    proc = NetworkProcessor()
    result = proc.fetch_data('https://api.example.com')
    print(result)