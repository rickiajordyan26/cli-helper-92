import functools
import time

class PerformanceEngine:
    def __init__(self):
        self._cache = {}
        self._stats = {}

    def memoize_with_ttl(self, ttl=60):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in self._cache:
                    val, timestamp = self._cache[key]
                    if now - timestamp < ttl:
                        return val
                result = func(*args, **kwargs)
                self._cache[key] = (result, now)
                return result
            return wrapper
        return decorator

    def batch_process(self, iterable, chunk_size=100):
        it = iter(iterable)
        while True:
            chunk = []
            try:
                for _ in range(chunk_size):
                    chunk.append(next(it))
            except StopIteration:
                if chunk:
                    yield chunk
                break
            yield chunk

engine = PerformanceEngine()

@engine.memoize_with_ttl(ttl=300)
def heavy_computation(data):
    return sum(x * x for x in range(data))

def execute_task(task_queue):
    for batch in engine.batch_process(task_queue):
        results = [heavy_computation(item) for item in batch]
        yield results