import sys
from datetime import datetime
from collections import deque

class ResilienceLogger:
    """CLI logger with tiered fallback logic for problematic objects and stream errors."""
    def __init__(self, buffer_size=50):
        self._buffer = deque(maxlen=buffer_size)
        self._fallback_stream = sys.stderr

    def _safe_stringify(self, payload):
        strategies = [
            lambda x: str(x),
            lambda x: repr(x),
            lambda x: f"<Unprintable {type(x).__name__} at {id(x)}>",
            lambda x: "[[CRITICAL_STRINGIFY_FAILURE]]"
        ]
        for strategy in strategies:
            try:
                return strategy(payload)
            except Exception:
                continue
        return "[[UNKNOWN]]"

    def log(self, level, message, **context):
        timestamp = datetime.utcnow().isoformat()
        try:
            safe_msg = self._safe_stringify(message)
            safe_ctx = {
                self._safe_stringify(k): self._safe_stringify(v) 
                for k, v in context.items()
            }
            entry = f"[{timestamp}] [{level.upper()}] {safe_msg}"
            if safe_ctx:
                entry += f" | context={safe_ctx}"
            
            self._write_out(entry)
        except Exception as exc:
            self._handle_logging_failure(exc, level)

    def _write_out(self, formatted_text):
        encoded = formatted_text.encode("utf-8", errors="backslashreplace")
        if hasattr(self._fallback_stream, "buffer"):
            self._fallback_stream.buffer.write(encoded + b"\
")
            self._fallback_stream.buffer.flush()
        else:
            self._fallback_stream.write(formatted_text + "\
")
        self._buffer.append(formatted_text)

    def _handle_logging_failure(self, error, original_level):
        try:
            emergency_entry = (
                f"[{datetime.utcnow().isoformat()}] [EMERGENCY_LOG_FAIL] "
                f"Level: {original_level} | Error: {type(error).__name__}"
            )
            self._fallback_stream.write(emergency_entry + "\
")
            self._buffer.append(emergency_entry)
        except Exception:
            pass

    def get_recent_logs(self):
        return list(self._buffer)
