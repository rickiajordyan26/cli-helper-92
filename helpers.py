import os
from typing import Callable, Union

class StyledText:
    """An operator-overloaded pipelining string formatter for CLI environments."""
    def __init__(self, text: str):
        self.text = text

    def __lshift__(self, modifier: Union[Callable[[str], str], str]) -> 'StyledText':
        if isinstance(modifier, str):
            colors = {
                "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
                "blue": "\033[34m", "bold": "\033[1m", "reset": "\033[0m"
            }
            code = colors.get(modifier.lower(), "")
            if code:
                self.text = f"{code}{self.text}{colors['reset']}"
        elif callable(modifier):
            self.text = modifier(self.text)
        return self

    def __str__(self) -> str:
        return self.text

def fit_terminal(padding: int = 4) -> Callable[[str], str]:
    """Dynamic truncator adjusting to live standard output columns."""
    def truncator(text: str) -> str:
        try:
            width = os.get_terminal_size().columns
        except (AttributeError, OSError):
            width = 80
        limit = max(10, width - padding)
        return text[:limit - 3] + "..." if len(text) > limit else text
    return truncator

def box_layout(text: str) -> str:
    """Renders target text wrapped inside a neat ASCII border."""
    lines = text.splitlines()
    max_len = max((len(line) for line in lines), default=0)
    border = f"+{'-' * (max_len + 2)}+"
    boxed = [border] + [f"| {line.ljust(max_len)} |" for line in lines] + [border]
    return "\n".join(boxed)
