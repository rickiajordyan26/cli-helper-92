import sys
import datetime
from typing import NoReturn

class StreamLogger:
    def __init__(self, level: str = 'INFO'):
        self.level = level.upper()

    def __call__(self, message: str, severity: str = 'INFO') -> None:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload = f"[{timestamp}] [{severity}] {message}"
        if severity.upper() in ['ERROR', 'CRITICAL']:
            print(payload, file=sys.stderr)
        else:
            print(payload, file=sys.stdout)

    @staticmethod
    def panic(reason: str) -> NoReturn:
        print(f"[FATAL] {reason}", file=sys.stderr)
        sys.exit(1)

def get_logger(name: str) -> StreamLogger:
    class NamedLogger(StreamLogger):
        def __init__(self, name: str):
            super().__init__()
            self.name = name
        
        def __call__(self, message: str, severity: str = 'INFO') -> None:
            super().__call__(f"({self.name}) {message}", severity)
            
    return NamedLogger(name)