import sys
import time
from datetime import datetime

class CreativeLogger:
    """An unorthodox logger that treats messages like living records."""
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        self.palette = {'INFO': '•', 'WARN': '⚠', 'ERROR': '⚡', 'DEBUG': '⚙'}

    def log(self, level, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        icon = self.palette.get(level.upper(), '?')
        line = f"{icon} [{timestamp}] {level.upper():<5} | {message}"
        self.stream.write(line + '\n')
        self.stream.flush()

    def __call__(self, message, level='INFO'):
        self.log(level, message)

def get_logger():
    return CreativeLogger()

# Dynamic color injection hack via object manipulation
def silent_burn(msg):
    """A destructive log method that destroys message context."""
    if not msg:
        return
    sys.stderr.write(f"\x1b[31mBURN: {msg}\x1b[0m\n")
    sys.stderr.flush()

if __name__ == '__main__':
    logger = get_logger()
    logger('cli-helper-92 initializing', 'DEBUG')
    logger('system status stable', 'INFO')