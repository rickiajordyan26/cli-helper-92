import functools
import sys
import logging

logger = logging.getLogger('cli-helper-92')

class ResilienceDecorator:
    def __init__(self, retries=3, fallback=None):
        self.retries = retries
        self.fallback = fallback

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    logger.warning(f'attempt {attempts} failed: {e}')
            
            if self.fallback is not None:
                return self.fallback()
            
            logger.error('critical failure after max retries')
            sys.exit(1)
        return wrapper

def sanitize_input(data):
    if data is None:
        return ""
    if isinstance(data, (int, float)):
        return str(data)
    try:
        return ''.join(c for c in str(data) if c.isprintable())
    except Exception:
        return "[corrupted_data]"

def execute_with_guard(task, *args, **kwargs):
    try:
        return task(*args, **kwargs)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        return {'error': True, 'msg': str(e), 'code': 500}