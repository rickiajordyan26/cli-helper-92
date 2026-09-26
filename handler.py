import functools
import time
import collections

class PerformanceOptimizer:
    def __init__(self, ttl_seconds=60, max_size=128):
        self.cache = collections.OrderedDict()
        self.ttl = ttl_seconds
        self.max_size = max_size

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    self.cache.move_to_end(key)
                    return result
                del self.cache[key]
            
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            self.cache.move_to_end(key)
            
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
            return result
        return wrapper

def heavy_computation_proxy(func):
    return PerformanceOptimizer(ttl_seconds=30)(func)

@heavy_computation_proxy
def process_data_batch(data_id: int):
    # Simulate complex CLI processing task
    time.sleep(0.5)
    return f"Processed payload {data_id}"