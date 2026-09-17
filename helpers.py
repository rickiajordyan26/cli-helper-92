import time
import functools
import random

def exponential_retry(max_attempts=3, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def network_action(func):
    """Wrapper to decorate network calls with retry behavior."""
    return exponential_retry(max_attempts=5, base_delay=0.5)(func)

# Example usage for CLI operations
@network_action
def fetch_resource(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError("Temporary server glitch")
    return f"Payload from {url}"