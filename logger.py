import sys
import datetime
from functools import wraps

class CreativeLogger:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        self.colors = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'END': '\033[0m'}

    def log(self, level, message):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.colors.get(level, '')
        print(f"{color}[{level}] {ts} | {message}{self.colors['END']}", file=self.stream)

    def trace_execution(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.log('INFO', f"entering {func.__name__} with {args}")
            try:
                result = func(*args, **kwargs)
                self.log('INFO', f"exiting {func.__name__} with result {result}")
                return result
            except Exception as e:
                self.log('ERROR', f"{func.__name__} crashed: {e}")
                raise
        return wrapper

def get_logger():
    return CreativeLogger()

# Usage:
# log = get_logger()
# @log.trace_execution
# def example(x): return x * 2