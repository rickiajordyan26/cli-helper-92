import json
import re
from typing import Any, Callable, List, Union

class StreamPipe:
    """Fluent operator-overloaded pipeline wrapper for CLI stream processing."""
    def __init__(self, data: Any = None):
        self._data = data

    def __ror__(self, left: Any) -> 'StreamPipe':
        return StreamPipe(left)

    def __or__(self, func: Callable[[Any], Any]) -> 'StreamPipe':
        if callable(func):
            if isinstance(self._data, (list, tuple)):
                return StreamPipe([func(item) for item in self._data])
            return StreamPipe(func(self._data))
        return self

    def unwrap(self) -> Any:
        return self._data

    def __str__(self) -> str:
        return str(self._data)


def strip_ansi(text: str) -> str:
    """Removes ANSI color and formatting escape codes from string data."""
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', str(text))


def truncate(length: int = 40, tail: str = "...") -> Callable[[Any], str]:
    """Creates a function that truncates strings to specified length."""
    def _truncator(val: Any) -> str:
        text = str(val)
        return text[:max(0, length - len(tail))] + tail if len(text) > length else text
    return _truncator


def ascii_box(header: str = "") -> Callable[[Any], str]:
    """Creates a function that wraps text inside a formatted ASCII frame."""
    def _boxer(val: Any) -> str:
        lines = str(val).splitlines() or [""]
        width = max(max(len(line) for line in lines), len(header)) + 2
        top = f"+--{header:-^{width-2}}--+" if header else f"+{'-' * (width + 2)}+"
        bottom = f"+{'-' * (width + 2)}+"
        body = [f"| {line:<{width}} |" for line in lines]
        return "\n".join([top] + body + [bottom])
    return _boxer


def auto_serialize(indent: int = 2) -> Callable[[Any], str]:
    """Creates a transformer for auto-formatting dicts or JSON strings."""
    def _serializer(val: Any) -> str:
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except json.JSONDecodeError:
                return val
        return json.dumps(val, indent=indent, default=str)
    return _serializer
