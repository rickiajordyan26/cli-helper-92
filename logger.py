import datetime
import sys
from typing import Any, NoReturn

class CLIConsoleLogger:
    """A whimsical yet functional logger for cli-helper-92."""

    def __init__(self, prefix: str = "[cli-92]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any) -> None:
        """Sends a message to stdout with a timestamp."""
        timestamp: str = datetime.datetime.now().strftime("%H:%M:%S")
        sys.stdout.write(f"{self.prefix} {timestamp} | {message}\n")

    def panic(self, reason: str) -> NoReturn:
        """Displays fatal error and exits the runtime."""
        sys.stderr.write(f"{self.prefix} FATAL: {reason}\n")
        sys.exit(1)

    def banner(self, text: str) -> None:
        """Prints a decorative separator for visual flair."""
        line: str = "=" * (len(text) + 4)
        sys.stdout.write(f"{line}\n= {text} =\n{line}\n")

def get_logger(name: str = "default") -> CLIConsoleLogger:
    """Factory for generating fresh logger instances."""
    return CLIConsoleLogger(prefix=f"[{name.upper()}]")