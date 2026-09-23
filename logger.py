import os
import sys
import time
from typing import Any, Dict


class DynamicCliLogger:
    """A minimal, self-metering CLI logger that tracks microsecond deltas
    between logs and formats outputs creatively based on terminal size.
    """

    COLORS: Dict[str, str] = {
        "DEBUG": "\033[90m",
        "INFO": "\033[36m",
        "SUCCESS": "\033[32m",
        "WARN": "\u001b[33m",
        "ERROR": "\033[31m",
        "RESET": "\033[0m",
    }

    def __init__(self, service_name: str = "CLI"):
        self.service_name = service_name
        self.last_log_time = time.perf_counter()

    def _get_delta(self) -> str:
        now = time.perf_counter()
        delta = now - self.last_log_time
        self.last_log_time = now
        if delta < 0.001:
            return f"{delta * 1_000_000:.0f}\u03bcs"
        elif delta < 1.0:
            return f"{delta * 1000:.1f}ms"
        return f"{delta:.2f}s"

    def log(self, level: str, message: str, *args: Any) -> None:
        level = level.upper()
        color = self.COLORS.get(level, self.COLORS["RESET"])
        delta_str = self._get_delta()

        try:
            columns, _ = os.get_terminal_size()
        except OSError:
            columns = 80

        formatted_msg = message % args if args else message
        prefix = f"[{self.service_name}] {color}{level:<7}{self.COLORS['RESET']}"
        suffix = f"({delta_str})"

        visible_prefix_len = len(self.service_name) + 11
        max_msg_len = columns - visible_prefix_len - len(suffix) - 5

        if max_msg_len > 10 and len(formatted_msg) > max_msg_len:
            formatted_msg = formatted_msg[:max_msg_len - 3] + "..."

        spacing = " " * max(1, columns - visible_prefix_len - len(formatted_msg) - len(suffix) - 4)
        sys.stdout.write(f"{prefix} | {formatted_msg}{spacing}{suffix}\n")
        sys.stdout.flush()

    def debug(self, msg: str, *args: Any) -> None:
        self.log("DEBUG", msg, *args)

    def info(self, msg: str, *args: Any) -> None:
        self.log("INFO", msg, *args)

    def success(self, msg: str, *args: Any) -> None:
        self.log("SUCCESS", msg, *args)

    def warn(self, msg: str, *args: Any) -> None:
        self.log("WARN", msg, *args)

    def error(self, msg: str, *args: Any) -> None:
        self.log("ERROR", msg, *args)
