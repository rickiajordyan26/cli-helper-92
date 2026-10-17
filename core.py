import functools
import time
import collections

class PerformanceOptimizer:
    def __init__(self, limit=128):
        self.limit = limit
        self.cache = collections.OrderedDict()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key not in self.cache:
                if len(self.cache) >= self.limit:
                    self.cache.popitem(last=False)
                self.cache[key] = func(*args, **kwargs)
            return self.cache[key]
        return wrapper

class LazyLoader:
    def __init__(self, target_func):
        self.target = target_func
        self.result = None
        self.initialized = False

    def __get__(self, instance, owner):
        if not self.initialized:
            self.result = self.target(instance)
            self.initialized = True
        return self.result

def batch_process(data, chunk_size=10):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

@PerformanceOptimizer(limit=256)
def heavy_computation(n):
    return sum(i * i for i in range(n))