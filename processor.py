import json
from typing import Any, Dict, Generator, Tuple, Union


class DataStreamProcessor:
    """Generator-based flattener and lookup engine for CLI data handling."""

    def __init__(self, delimiter: str = "."):
        self.delimiter = delimiter

    def flatten(self, data: Any, prefix: str = "") -> Generator[Tuple[str, Any], None, None]:
        """Recursively flattens arbitrarily nested data structures."""
        if isinstance(data, dict):
            for key, val in data.items():
                next_key = f"{prefix}{self.delimiter}{key}" if prefix else str(key)
                yield from self.flatten(val, next_key)
        elif isinstance(data, (list, tuple, set)):
            for index, item in enumerate(data):
                next_key = f"{prefix}[{index}]"
                yield from self.flatten(item, next_key)
        else:
            yield (prefix, data)

    def transform(self, data: Any, filter_term: Union[str, None] = None) -> Dict[str, Any]:
        """Transforms data into key-value map with optional fuzzy filter."""
        flattened = dict(self.flatten(data))
        if not filter_term:
            return flattened
        term = filter_term.lower()
        return {k: v for k, v in flattened.items() if term in k.lower() or term in str(v).lower()}


def format_for_display(payload: Any, filter_term: Union[str, None] = None) -> str:
    """Utility function to parse and format data for terminal output."""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            payload = {"text": payload}

    processor = DataStreamProcessor()
    results = processor.transform(payload, filter_term)

    if not results:
        return "No matching records found."

    max_key_len = max(len(k) for k in results.keys())
    return "\n".join(f"{k.ljust(max_key_len)} : {v}" for k, v in results.items())
