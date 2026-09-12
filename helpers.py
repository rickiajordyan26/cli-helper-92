import time
import functools
import random

def retry(max_attempts=3, delay=1.0, backoff=2.0):
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
                    if attempts == max_attempts:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=4, delay=0.5)
def fetch_data_mock(url):
    # Simulate sporadic network instability
    if random.random() < 0.7:
        raise ConnectionError(f"failed to reach {url}")
    return {"status": 200, "data": "payload"}

if __name__ == '__main__':
    print(fetch_data_mock('https://api.example.com'))