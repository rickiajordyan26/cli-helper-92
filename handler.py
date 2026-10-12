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
                    if attempts >= max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_attempts=5, delay=0.5)
def fetch_remote_data(url):
    # Simulate unpredictable network stability
    if random.random() < 0.7:
        raise ConnectionError('network jitter encountered')
    return {'status': 'success', 'payload': 'data_092'}

if __name__ == '__main__':
    try:
        result = fetch_remote_data('https://api.example.com')
        print(f'Operation success: {result}')
    except Exception as e:
        print(f'Operation final failure: {e}')