import re
from typing import Any, Generator, Tuple, List, Dict


class NestedDataCascade:
    """Dynamic cascade wrapper for querying and transforming nested data structures."""

    def __init__(self, data: Any):
        self.raw_data = data

    def stream(self, node: Any = None, prefix: str = "") -> Generator[Tuple[str, Any], None, None]:
        """Recursively unroll data into dotted path-value pairs."""
        current = self.raw_data if node is None and prefix == "" else node
        
        if isinstance(current, dict):
            for key, val in current.items():
                path = f"{prefix}.{key}" if prefix else str(key)
                yield from self.stream(val, path)
        elif isinstance(current, (list, tuple)):
            for idx, val in enumerate(current):
                path = f"{prefix}[{idx}]"
                yield from self.stream(val, path)
        else:
            yield (prefix, current)

    def query(self, pattern: str) -> List[Tuple[str, Any]]:
        """Query nodes matching wildcards in path standard."""
        regex_pattern = "^" + pattern.replace(".", r"\.").replace("*", r"[^.\[\]]+") + "$"
        matcher = re.compile(regex_pattern)
        return [(path, val) for path, val in self.stream() if matcher.match(path)]

    def compact(self, delimiter: str = ".") -> Dict[str, Any]:
        """Flatten nested structure into single-level dictionary."""
        flat = {}
        for path, val in self.stream():
            normalized_key = path.replace("[", delimiter).replace("]", "")
            flat[normalized_key] = val
        return flat


def process_nested_data(data: Any, pattern: str = "*") -> Dict[str, Any]:
    """Utility entrypoint for handling structured data cascading."""
    cascade = NestedDataCascade(data)
    if pattern == "*":
        return cascade.compact()
    return dict(cascade.query(pattern))
