import sys
import shutil
import textwrap
from typing import Any, Callable, Dict


class CliPipe:
    """A lightweight pipe wrapper enabling chainable CLI operations."""

    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Callable[[Any], Any]) -> "CliPipe":
        return CliPipe(func(self.value))

    def __str__(self) -> str:
        return str(self.value)

    def emit(self, stream=sys.stdout) -> None:
        stream.write(f"{self.value}\n")


def truncate(width: int = 0) -> Callable[[str], str]:
    cols = width or shutil.get_terminal_size().columns
    return lambda text: textwrap.shorten(str(text), width=cols, placeholder="...")


def colorize(code: int) -> Callable[[str], str]:
    return lambda text: f"\033[{code}m{text}\033[0m"


def banner(char: str = "=") -> Callable[[str], str]:
    def _wrap(text: str) -> str:
        cols = shutil.get_terminal_size().columns
        line = char * cols
        return f"{line}\n{str(text).center(cols)}\n{line}"

    return _wrap


def kv_table(indent: int = 2) -> Callable[[Dict[str, Any]], str]:
    def _format(data: Dict[str, Any]) -> str:
        if not data:
            return ""
        max_k = max(len(str(k)) for k in data.keys())
        pad = " " * indent
        return "\n".join(
            f"{pad}{str(k).ljust(max_k)} : {v}" for k, v in data.items()
        )

    return _format


def pipeline(value: Any) -> CliPipe:
    return CliPipe(value)
