import time
from functools import lru_cache

class PerformanceLogger:
    _buffer = []

    def __init__(self, limit=1000):
        self.limit = limit

    @staticmethod
    @lru_cache(maxsize=128)
    def _format_timestamp(ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))

    def log(self, message):
        entry = f"[{self._format_timestamp(time.time())}] {message}"
        self._buffer.append(entry)
        if len(self._buffer) > self.limit:
            self._flush()

    def _flush(self):
        with open('app.log', 'a') as f:
            f.write('\n'.join(self._buffer) + '\n')
        self._buffer.clear()

    def __del__(self):
        if self._buffer:
            self._flush()