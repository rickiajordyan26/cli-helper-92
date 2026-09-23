import functools
import time
import collections

class MemoizeWithTTL:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}
        self.expires = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache and now < self.expires.get(key, 0):
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.expires[key] = now + self.ttl
            return result
        return wrapper

class FastProcessor:
    def __init__(self, limit=1000):
        self.buffer = collections.deque(maxlen=limit)

    def batch_process(self, data, func):
        results = []
        for item in data:
            if item in self.buffer:
                results.append(self.buffer[self.buffer.index(item)])
                continue
            res = func(item)
            self.buffer.append(res)
            results.append(res)
        return results

@MemoizeWithTTL(ttl=300)
def expensive_transformation(value):
    time.sleep(0.5)
    return value * 2

def get_optimized_data(items):
    processor = FastProcessor()
    return processor.batch_process(items, expensive_transformation)