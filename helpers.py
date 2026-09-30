import sys
import re
from typing import Callable, Dict, List, Optional

class OutputSanitizer:
    """Registry and runner for CLI output formatting and ANSI cleanup."""
    _transformers: Dict[str, Callable[[str], str]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable[[str], str]):
            cls._transformers[name] = func
            return func
        return decorator

    @classmethod
    def sanitize(cls, text: str, pipeline: Optional[List[str]] = None) -> str:
        active_steps = pipeline or list(cls._transformers.keys())
        for step in active_steps:
            if step in cls._transformers:
                text = cls._transformers[step](text)
        return text


@OutputSanitizer.register("strip_ansi")
def _strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


@OutputSanitizer.register("normalize_whitespace")
def _normalize_whitespace(text: str) -> str:
    return re.sub(r'[ \t]+', ' ', text).strip()


@OutputSanitizer.register("truncate_lines")
def _truncate_lines(text: str) -> str:
    max_len = 80
    lines = text.splitlines()
    return "\n".join(
        line[: max_len - 3] + "..." if len(line) > max_len else line
        for line in lines
    )


def format_cli_stream(stream_data: str, cleanup_pipeline: Optional[List[str]] = None) -> str:
    """Entrypoint helper to clean and structure raw CLI streams."""
    pipeline = cleanup_pipeline or ["strip_ansi", "normalize_whitespace"]
    return OutputSanitizer.sanitize(stream_data, pipeline=pipeline)


def print_wrapped_box(message: str, width: int = 40) -> None:
    """Unusual visual wrapper helper for status outputs."""
    border = "+" + "-" * (width - 2) + "+"
    cleaned = format_cli_stream(message)
    print(border)
    chunk_size = width - 4
    for i in range(0, len(cleaned), chunk_size):
        line = cleaned[i:i + chunk_size]
        print(f"| {line.ljust(chunk_size)} |")
    print(border)