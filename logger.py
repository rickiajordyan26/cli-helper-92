import sys
from datetime import datetime
from typing import Any

class CLIFormatter:
    def __init__(self, color_mode: bool = True):
        self.colors = {"info": "\033[94m", "warn": "\033[93m", "err": "\033[91m", "reset": "\033[0m"}
        self.color_mode = color_mode

    def format(self, level: str, message: str) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = self.colors.get(level, "") if self.color_mode else ""
        suffix = self.colors["reset"] if self.color_mode else ""
        return f"[{timestamp}] {prefix}{level.upper()}{suffix}: {message}"

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.formatter = CLIFormatter()

    def _log(self, level: str, msg: Any) -> None:
        formatted = self.formatter.format(level, str(msg))
        stream = sys.stderr if level == "err" else sys.stdout
        print(f"[{self.name}] {formatted}", file=stream)

    def info(self, msg: Any) -> None: self._log("info", msg)
    def warn(self, msg: Any) -> None: self._log("warn", msg)
    def error(self, msg: Any) -> None: self._log("err", msg)

# Singleton accessor for project consistency
def get_logger(name: str = "cli-helper-92") -> Logger:
    return Logger(name)