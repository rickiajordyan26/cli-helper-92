"""Terminal text styling and pipeline transformation utilities for CLI interfaces."""

from typing import Callable, Iterable, Generator, Any, Self, TypeVar

T = TypeVar("T")

class AnsiPipeline:
    """An overload-heavy string formatter for terminal pipelines.
    
    Allows chaining ANSI color codes and transformations using bitwise OR `|`
    and shift `>>` operators for creative terminal stream formatting.
    """

    CODES: dict[str, str] = {
        "bold": "\033[1m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "reset": "\033[0m",
    }

    def __init__(self, text: str = "") -> None:
        self.text: str = text
        self._styles: list[str] = []

    def __or__(self, style_name: str) -> Self:
        """Applies a named ANSI code style to the pipeline instance via `|`."""
        if style_name in self.CODES:
            self._styles.append(self.CODES[style_name])
        return self

    def __rshift__(self, transform: Callable[[str], str]) -> Self:
        """Applies a string transformation function using the `>>` operator."""
        self.text = transform(self.text)
        return self

    def render(self) -> str:
        """Renders the final styled string wrapped with ANSI escape sequences."""
        prefix = "".join(self._styles)
        suffix = self.CODES["reset"] if self._styles else ""
        return f"{prefix}{self.text}{suffix}"

    def __str__(self) -> str:
        return self.render()


def format_stream(items: Iterable[Any], style: str = "green") -> Generator[str, None, None]:
    """Yields stream items decorated as styled string pipeline outputs.

    Args:
        items: An iterable collection of raw objects to format.
        style: The name of the ANSI color style to apply.

    Yields:
        Rendered ANSI strings for terminal output.
    """
    for item in items:
        pipeline = AnsiPipeline(str(item)) | style | "bold"
        yield pipeline.render()


def smart_truncate(text: str, max_len: int = 20) -> str:
    """Truncates text nicely with an ellipsis if it exceeds length limit."""
    return text[: max_len - 3] + "..." if len(text) > max_len else text
