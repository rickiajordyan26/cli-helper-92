"""CLI formatting and stream transformation utilities for cli-helper-92."""

import textwrap
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)

T = TypeVar("T")
R = TypeVar("R")


def rainbow_wrap(
    text: str, width: int = 40, prefix_char: str = "│ "
) -> Generator[str, None, None]:
    """Wraps text into a visual panel using ANSI color steps across lines.

    Args:
        text: Raw text string to wrap and format.
        width: Maximum characters per line before wrapping.
        prefix_char: Margin decoration prefix for each line.

    Yields:
        Formatted line strings prefixed with an ANSI color sequence.
    """
    ansi_colors: List[int] = [31, 33, 32, 36, 34, 35]
    wrapped_lines: List[str] = textwrap.wrap(text, width=width) or [""]
    for idx, line in enumerate(wrapped_lines):
        color_code: int = ansi_colors[idx % len(ansi_colors)]
        yield f"\033[{color_code}m{prefix_char}\033[0m{line}"


class ExecutionPipeline:
    """A fluent function composition runner for CLI data transformations."""

    def __init__(self, initial_value: Any) -> None:
        """Initialize the pipeline with a starting data payload."""
        self._value: Any = initial_value

    def pipe(self, fn: Callable[[Any], Any]) -> "ExecutionPipeline":
        """Apply a mapping function to the encapsulated payload.

        Args:
            fn: Transformation function accepting current payload.

        Returns:
            Updated ExecutionPipeline instance for method chaining.
        """
        self._value = fn(self._value)
        return self

    def collect(self) -> Any:
        """Unwrap and return the final computed pipeline state."""
        return self._value


def format_cli_output(
    data: Union[str, Iterable[str]],
    banner: Optional[str] = None,
    width: int = 50,
) -> str:
    """Formats raw text or iterable lines into a stylized CLI block output.

    Args:
        data: String content or iterable of string tokens to join.
        banner: Optional header title to display above the block.
        width: Desired column width for visual bounds.

    Returns:
        Fully composed multi-line CLI display string.
    """
    payload: str = " ".join(data) if not isinstance(data, str) else data
    header: str = f"=== {banner} ===" if banner else "=" * width

    pipeline = (
        ExecutionPipeline(payload)
        .pipe(lambda text: rainbow_wrap(str(text), width=width))
        .pipe(lambda gen: "\n".join(gen))
    )

    body: str = str(pipeline.collect())
    return f"{header}\n{body}\n{'=' * len(header)}"
