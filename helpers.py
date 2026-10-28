import shutil
from typing import Callable, Union


class TextCanvas:
    """Fluent operator-overloaded text helper for CLI formatting pipelines."""

    def __init__(self, text: str = ""):
        self._lines = text.splitlines() if text else []

    def __add__(self, other: Union[str, "TextCanvas"]) -> "TextCanvas":
        other_lines = (
            other._lines if isinstance(other, TextCanvas) else str(other).splitlines()
        )
        res = TextCanvas()
        res._lines = self._lines + other_lines
        return res

    def __or__(self, transform: Callable[[str], str]) -> "TextCanvas":
        res = TextCanvas()
        res._lines = [transform(line) for line in self._lines]
        return res

    def box(self, padding: int = 1) -> "TextCanvas":
        if not self._lines:
            return TextCanvas("┌┐\n└┘")
        width = max(len(line) for line in self._lines)
        top = f"┌{'─' * (width + padding * 2)}┐"
        bottom = f"└{'─' * (width + padding * 2)}┘"
        pad = " " * padding
        framed = [
            f"│{pad}{line.ljust(width)}{pad}│" for line in self._lines
        ]
        res = TextCanvas()
        res._lines = [top] + framed + [bottom]
        return res

    def render(self) -> str:
        return "\n".join(self._lines)

    def __str__(self) -> str:
        return self.render()


def get_terminal_width(default: int = 80) -> int:
    return shutil.get_terminal_size((default, 24)).columns


def truncate_middle(text: str, max_len: int = 30, middle: str = "...") -> str:
    if len(text) <= max_len:
        return text
    margin = max(1, (max_len - len(middle)) // 2)
    return f"{text[:margin]}{middle}{text[-margin:]}"


def render_progress_bar(current: int, total: int, width: int = 20) -> str:
    ratio = min(1.0, max(0.0, current / max(total, 1)))
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {ratio * 100:5.1f}%"
