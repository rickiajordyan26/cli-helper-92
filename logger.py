import sys
from typing import Dict, Tuple, Deque
from collections import deque
from datetime import datetime

class CliLogger:
    """
    A whimsical yet sturdy CLI logger that maintains a circular buffer of
    low-priority diagnostic logs, printing them post-factum only if an error occurs.
    """
    def __init__(self, name: str, buffer_size: int = 10) -> None:
        self.name: str = name
        self._buffer: Deque[Tuple[str, str]] = deque(maxlen=buffer_size)
        self._severity_emojis: Dict[str, str] = {
            "DEBUG": "🔍",
            "INFO": "✨",
            "WARNING": "⚠️",
            "ERROR": "💥",
            "CRITICAL": "🚨"
        }

    def _format(self, level: str, message: str) -> str:
        """Formats the message with a timestamp and a thematic emoji."""
        timestamp: str = datetime.now().isoformat(timespec="seconds")
        emoji: str = self._severity_emojis.get(level, "📝")
        return f"[{timestamp}] {emoji} {level:<8} | {self.name} | {message}"

    def log(self, level: str, message: str) -> None:
        """
        Dispatches logs directly to stdout/stderr, or buffers them
        if they are diagnostic (DEBUG/INFO) to keep the CLI clean.
        """
        formatted: str = self._format(level, message)
        if level in ("DEBUG", "INFO"):
            self._buffer.append((level, formatted))
        else:
            if level in ("ERROR", "CRITICAL") and self._buffer:
                sys.stderr.write("--- RETROSPECTIVE DIAGNOSTIC DUMP ---\n")
                while self._buffer:
                    _, old_msg = self._buffer.popleft()
                    sys.stderr.write(f"  (buffered) {old_msg}\n")
                sys.stderr.write("--- END OF DIAGNOSTIC DUMP ---\n")
            
            stream = sys.stderr if level in ("WARNING", "ERROR", "CRITICAL") else sys.stdout
            stream.write(formatted + "\n")
            stream.flush()

    def debug(self, message: str) -> None:
        """Logs a message with DEBUG severity (buffered)."""
        self.log("DEBUG", message)

    def info(self, message: str) -> None:
        """Logs a message with INFO severity (buffered)."""
        self.log("INFO", message)

    def warning(self, message: str) -> None:
        """Logs a warning directly to stderr."""
        self.log("WARNING", message)

    def error(self, message: str) -> None:
        """Logs an error, dumping any buffered debug/info statements first."""
        self.log("ERROR", message)