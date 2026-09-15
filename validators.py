import functools
import time

_memoized_cache = {}

def lru_cache_with_ttl(ttl_seconds=60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in _memoized_cache:
                result, timestamp = _memoized_cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            _memoized_cache[key] = (result, now)
            return result
        return wrapper
    return decorator

@lru_cache_with_ttl(ttl_seconds=300)
def validate_input_schema(data_packet):
    if not isinstance(data_packet, dict):
        return False
    return all(isinstance(k, str) for k in data_packet.keys())

def bulk_validate(data_list):
    # Vectorized-style evaluation for heavy processing modules
    results = map(validate_input_schema, data_list)
    return list(results)

def flush_cache():
    _memoized_cache.clear()