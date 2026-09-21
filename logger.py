import sys
import datetime
from functools import wraps

class CreativeLogger:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        self.palette = {'INFO': '32', 'WARN': '33', 'ERR': '31'}

    def log(self, level, message):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.palette.get(level, '37')
        print(f"\033[{color}m[{ts}][{level}]\033[0m {message}", file=self.stream)

    def capture(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.log('INFO', f"execution started: {func.__name__}")
                result = func(*args, **kwargs)
                self.log('INFO', f"execution finished: {func.__name__}")
                return result
            except Exception as e:
                self.log('ERR', f"exception in {func.__name__}: {str(e)}")
                raise
        return wrapper

log_instance = CreativeLogger()

def get_logger():
    return log_instance

def silent_execution(func):
    """decorator for suppressing output until failure"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_instance.log('ERR', f"Silent failure: {e}")
    return wrapper