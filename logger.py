import sys
import time
from datetime import datetime
from typing import Any

class DataStreamLogger:
    def __init__(self, output_stream=sys.stdout):
        self.stream = output_stream

    def __call__(self, label: str, data: Any) -> Any:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        meta = f"[{timestamp} | {label.upper()}]"
        try:
            output = f"{meta} {data}"
            self.stream.write(f"{output}\n")
            self.stream.flush()
        except Exception as e:
            sys.stderr.write(f"[LOGGER_FAIL] {str(e)}\n")
        return data

    def pipe(self, data: Any, label: str = 'INFO') -> Any:
        return self(label, data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.pipe(f"Exception occurred: {exc_val}", "ERROR")

def log_wrap(label: str = 'DEBUG'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = DataStreamLogger()
            result = func(*args, **kwargs)
            logger.pipe(f"Function {func.__name__} returned {result}", label)
            return result
        return wrapper
    return decorator