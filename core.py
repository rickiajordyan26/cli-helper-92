import time
import random
from functools import wraps

def resilient_network_call(max_attempts=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@resilient_network_call(max_attempts=4)
def fetch_remote_data(endpoint):
    # Simulate volatile network operation
    if random.random() < 0.7:
        raise ConnectionError("Transient network glitch")
    return {"status": 200, "payload": "data_payload"}

if __name__ == '__main__':
    try:
        print(fetch_remote_data("https://api.example.com"))
    except Exception as err:
        print(f"Operation failed after retries: {err}")