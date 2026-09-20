import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_operation(attempts=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        logger.error(f"Final attempt failed: {e}")
                        raise
                    logger.warning(f"Attempt {i+1} failed, retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(attempts=3)
def fetch_url(url):
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read().decode('utf-8')