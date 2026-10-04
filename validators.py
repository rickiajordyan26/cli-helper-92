import time
import functools
import random

def retry_operation(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=4, delay=0.5)
def ping_service(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError(f"service at {url} unreachable")
    return True