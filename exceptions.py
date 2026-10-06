import functools
import time
import logging

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.hit_counts = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self.cache:
                self.hit_counts[key] = self.hit_counts.get(key, 0) + 1
                return self.cache[key]
            
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            
            if duration > 0.05:
                logging.debug(f'Slow execution detected in {func.__name__}: {duration:.4f}s')
            
            self.cache[key] = result
            return result
        return wrapper

class CoreOptimizationError(Exception):
    """Custom exception for performance-related bottlenecks."""
    def __init__(self, message, metadata=None):
        super().__init__(message)
        self.metadata = metadata or {}

memoize_optimized = PerformanceOptimizer()