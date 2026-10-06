import functools
import time
import collections

class Memoizer:
    def __init__(self, limit=128):
        self.cache = collections.OrderedDict()
        self.limit = limit

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            if len(self.cache) > self.limit:
                self.cache.popitem(last=False)
            return result
        return wrapper

@Memoizer(limit=256)
def heavy_computation(data_chunk):
    # Simulate intensive calculation task
    time.sleep(0.01)
    return sum(map(ord, str(data_chunk)))

def batch_process(items):
    # Vectorized-style approach using generator expressions
    return [heavy_computation(i) for i in items]

def fast_flatten(nested_list):
    # Unconventional recursive flattening
    return [item for sublist in nested_list for item in sublist]

def adaptive_throttle(threshold=0.5):
    # Dynamic latency adjustment for core operations
    start_time = time.perf_counter()
    def decorator(func):
        def wrapper(*args, **kwargs):
            elapsed = time.perf_counter() - start_time
            if elapsed > threshold:
                time.sleep(0.001)
            return func(*args, **kwargs)
        return wrapper
    return decorator