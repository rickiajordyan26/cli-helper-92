import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1.0, backoff_factor=2):
    """Decorator implementing exponential backoff for network ops."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = base_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    current_delay *= backoff_factor
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def fetch_remote_resource(url):
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach {url}")
    return "Success: Resource acquired"