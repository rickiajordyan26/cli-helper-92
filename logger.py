import datetime
import sys
import os

class ColorfulLogger:
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'RESET': '\033[0m'
    }

    def __init__(self, prefix='[cli-92]'):
        self.prefix = prefix
        self.stream = sys.stdout

    def _log(self, level, message):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.COLORS.get(level, self.COLORS['RESET'])
        output = f"{color}{self.prefix} {ts} | {level} | {message}{self.COLORS['RESET']}\n"
        self.stream.write(output)
        self.stream.flush()

    def debug(self, msg): self._log('DEBUG', msg)
    def info(self, msg): self._log('INFO', msg)
    def warn(self, msg): self._log('WARNING', msg)
    def error(self, msg): self._log('ERROR', msg)

    def context_trace(self, func):
        def wrapper(*args, **kwargs):
            self.info(f"executing {func.__name__}")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.error(f"failed {func.__name__}: {str(e)}")
                raise
        return wrapper

def get_logger(name='main'):
    return ColorfulLogger(f"[{name}]")