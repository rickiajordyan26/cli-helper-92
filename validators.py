import functools
import time

class MemoizedValidator:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                res, ts = self.cache[key]
                if now - ts < self.ttl:
                    return res
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def fast_input_check(func):
    cache = {}
    def inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return inner

@MemoizedValidator(ttl=60)
def validate_config_schema(schema_id: str) -> bool:
    # Simulate expensive regex validation
    time.sleep(0.5)
    return schema_id.startswith('v_') and len(schema_id) > 5

@fast_input_check
def validate_permission_level(level: int) -> bool:
    return 0 <= level <= 100