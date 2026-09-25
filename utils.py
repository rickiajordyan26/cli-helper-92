import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_operation(max_attempts=3, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = 1
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f'failed after {attempts} attempts')
                        raise
                    logger.warning(f'retry {attempts}/{max_attempts} after error: {e}')
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

@retry_operation(max_attempts=3)
def fetch_network_resource(url):
    # Simulate network instability
    import random
    if random.random() < 0.7:
        raise ConnectionError('intermittent network failure')
    return f'data from {url}'