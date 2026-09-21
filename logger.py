import sys
import time
from functools import lru_cache

class AsyncBufferLogger:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.buffer = []
        self._last_flush = time.monotonic()

    @lru_cache(maxsize=128)
    def _format_timestamp(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    def log(self, level, message):
        entry = f"[{self._format_timestamp(time.time())}] {level.upper()}: {message}"
        self.buffer.append(entry)
        
        if len(self.buffer) >= self.capacity or (time.monotonic() - self._last_flush) > 5:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
        sys.stdout.write('\n'.join(self.buffer) + '\n')
        sys.stdout.flush()
        self.buffer.clear()
        self._last_flush = time.monotonic()

    def __del__(self):
        self.flush()

def get_logger():
    if not hasattr(get_logger, '_instance'):
        get_logger._instance = AsyncBufferLogger()
    return get_logger._instance