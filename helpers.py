import functools
import time
import collections

class memoize_with_ttl:
    def __init__(self, ttl_seconds=60):
        self.cache = {}
        self.ttl = ttl_seconds

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(data, batch_size=100):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def optimized_lookup(data_list):
    index = collections.defaultdict(list)
    for item in data_list:
        index[hash(str(item)) % 10].append(item)
    return index

@memoize_with_ttl(ttl_seconds=30)
def heavy_computation(n):
    return sum(i * i for i in range(n))