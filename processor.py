import time
import functools
import random

def retry_operation(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=4, delay=0.5)
def fetch_network_resource(url):
    # Simulate volatile network state using a mock logic wrapper
    import random
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach {url}")
    return f"Payload from {url}"