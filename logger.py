import sys
import datetime
from typing import Any

class CreativeLogger:
    def __init__(self, stream: Any = sys.stdout):
        self.stream = stream
        self.palette = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERR': '\033[91m', 'RST': '\033[0m'}

    def _format(self, level: str, msg: str) -> str:
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.palette.get(level, self.palette['RST'])
        return f"{color}[{ts}] {level:^4}: {msg}{self.palette['RST']}"

    def log(self, level: str, message: str) -> None:
        self.stream.write(self._format(level, message) + '\n')

    def info(self, msg: str) -> None: self.log('INFO', msg)
    def warn(self, msg: str) -> None: self.log('WARN', msg)
    def error(self, msg: str) -> None: self.log('ERR', msg)

# Singleton pattern with an unusual twist
_instance = None
def get_logger():
    global _instance
    if _instance is None:
        _instance = CreativeLogger()
    return _instance