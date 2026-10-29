import time
import functools
import random

def retry_operation(retries=3, backoff=1.0, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == retries:
                        raise e
                    wait = backoff * (2 ** (attempts - 1))
                    if jitter:
                        wait *= random.uniform(0.5, 1.5)
                    time.sleep(wait)
            return None
        return wrapper
    return decorator

@retry_operation(retries=5, backoff=0.5)
def fetch_url_content(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError("Temporary network glitch")
    return f"Successfully retrieved data from {url}"