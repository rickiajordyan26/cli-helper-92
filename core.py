import functools
import time
import collections

class PerformanceOptimizer:
    def __init__(self, cache_limit=128):
        self.cache_limit = cache_limit
        self._memo = {}
        self._hits = collections.Counter()

    def fast_track(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self._memo:
                self._hits[key] += 1
                return self._memo[key]
            
            result = func(*args, **kwargs)
            
            if len(self._memo) >= self.cache_limit:
                lru_key = self._hits.most_common()[-1][0]
                del self._memo[lru_key]
                del self._hits[lru_key]
            
            self._memo[key] = result
            self._hits[key] = 1
            return result
        return wrapper

def heavy_computation(n):
    time.sleep(0.1)
    return sum(i * i for i in range(n))

optimizer = PerformanceOptimizer(cache_limit=64)
optimized_compute = optimizer.fast_track(heavy_computation)

def process_batch(data_points):
    return [optimized_compute(n) for n in data_points]

if __name__ == '__main__':
    print(process_batch([1000, 2000, 1000]))