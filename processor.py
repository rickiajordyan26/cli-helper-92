import functools
import time
import itertools

def retry(attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator

def chunk_stream(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk: break
        yield chunk

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

class Pipeline:
    def __init__(self, *funcs):
        self.pipeline = compose(*funcs[::-1])
    
    def process(self, data):
        return self.pipeline(data)

def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]

def dict_invert(d):
    return {v: k for k, v in d.items()}