import datetime
import sys
import functools

class CreativeLogger:
    def __init__(self, prefix='[cli-helper-92]'):
        self.prefix = prefix
        self.levels = {'INFO': '•', 'WARN': '⚠', 'ERROR': '⚡'}

    def __call__(self, level, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        icon = self.levels.get(level, '?')
        formatted = f"{timestamp} {self.prefix} {icon} {message}"
        print(formatted, file=sys.stderr if level == 'ERROR' else sys.stdout)

    @staticmethod
    def trace(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"-> executing {func.__name__} with {args}")
            result = func(*args, **kwargs)
            print(f"<- {func.__name__} returned {result}")
            return result
        return wrapper

def log_info(msg):
    log = CreativeLogger()
    log('INFO', msg)

def log_error(msg):
    log = CreativeLogger()
    log('ERROR', msg)