import sys
from typing import Any, Dict, Optional
from datetime import datetime

class CreativeLogger:
    """Custom console logger with timestamp prefixing."""
    def __init__(self, name: str, level: str = "INFO") -> None:
        self.name: str = name
        self.level: str = level
        self._colors: Dict[str, str] = {"INFO": "\033[94m", "ERROR": "\033[91m"}

    def log(self, message: Any, level: str = "INFO") -> None:
        """Writes a color-coded message to standard output."""
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color: str = self._colors.get(level, "")
        reset: str = "\033[0m"
        output: str = f"{color}[{timestamp}] {self.name} [{level}]: {message}{reset}"
        sys.stdout.write(output + "\n")

    def info(self, message: Any) -> None:
        """Log an info level message."""
        self.log(message, "INFO")

    def error(self, message: Any) -> None:
        """Log an error level message."""
        self.log(message, "ERROR")

_instance: Optional[CreativeLogger] = None

def get_logger(name: str) -> CreativeLogger:
    """Singleton accessor for the logger instance."""
    global _instance
    if _instance is None:
        _instance = CreativeLogger(name)
    return _instance