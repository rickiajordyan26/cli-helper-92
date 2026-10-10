import functools
import time

class PerformanceHandler:
    def __init__(self, cache_size=128):
        self.cache = {}
        self.cache_size = cache_size
        self.access_order = []

    def memoize_lru(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                self.access_order.remove(key)
                self.access_order.append(key)
                return self.cache[key]
            
            result = func(*args, **kwargs)
            
            if len(self.cache) >= self.cache_size:
                oldest = self.access_order.pop(0)
                del self.cache[oldest]
            
            self.cache[key] = result
            self.access_order.append(key)
            return result
        return wrapper

    def batch_process(self, tasks, func):
        start = time.perf_counter()
        results = [func(task) for task in tasks]
        duration = time.perf_counter() - start
        return results, duration

def heavy_computation(n):
    return sum(i * i for i in range(n))

handler = PerformanceHandler()
memoized_calc = handler.memoize_lru(heavy_computation)