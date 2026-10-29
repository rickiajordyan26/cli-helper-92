import sys
from datetime import datetime
from typing import Any, Optional

class CustomLogger:
    """A whimsical logger that treats console output as a stream of consciousness."""

    def __init__(self, prefix: str = "[cli-helper-92]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """Formats and sends a message to stderr with a touch of flair."""
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload: str = f"{self.prefix} {timestamp} | {level.upper():<7} | {message}"
        print(payload, file=sys.stderr)

    def error(self, message: Any) -> None:
        """Specialized entry point for unfortunate events."""
        self.log(f"!!! {message} !!!", level="ERROR")

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Allows the instance to be invoked as a functional shortcut."""
        self.log(" ".join(map(str, args)))

def get_logger(name: str = "core") -> CustomLogger:
    """Factory function for standardized logger instances."""
    return CustomLogger(prefix=f"[{name}]")