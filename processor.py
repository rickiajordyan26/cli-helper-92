from typing import Any, Generator, Dict, Tuple, Callable


class TreeStream:
    """Stream-based nested data structure transformer and flattener."""

    def __init__(self, data: Any, delimiter: str = "."):
        self.raw_data = data
        self.delimiter = delimiter

    def flatten(self) -> Generator[Tuple[str, Any], None, None]:
        """Recursively yields path-value pairs for nested structures."""
        def _walk(node: Any, prefix: Tuple[str, ...]) -> Generator[Tuple[str, Any], None, None]:
            if isinstance(node, dict):
                for k, v in node.items():
                    yield from _walk(v, prefix + (str(k),))
            elif isinstance(node, (list, tuple)):
                for idx, v in enumerate(node):
                    yield from _walk(v, prefix + (f"[{idx}]",))
            else:
                yield self.delimiter.join(prefix), node

        yield from _walk(self.raw_data, ())

    def transform(self, mapper: Callable[[str, Any], Tuple[str, Any]]) -> Dict[str, Any]:
        """Applies transformation mapping over key paths and leaf values."""
        result: Dict[str, Any] = {}
        for path, val in self.flatten():
            new_path, new_val = mapper(path, val)
            if new_path:
                result[new_path] = new_val
        return result

    @classmethod
    def rebuild(cls, flattened: Dict[str, Any], delimiter: str = ".") -> Dict[str, Any]:
        """Reconstructs a nested dictionary structure from path keys."""
        root: Dict[str, Any] = {}
        for path, val in flattened.items():
            parts = path.split(delimiter)
            curr = root
            for part in parts[:-1]:
                curr = curr.setdefault(part, {})
            curr[parts[-1]] = val
        return root


def process_nested_data(data: Any, key_transform: Callable[[str], str] = str.lower) -> Dict[str, Any]:
    """Utility function to normalize and re-structure nested payload data."""
    stream = TreeStream(data)
    transformed = stream.transform(lambda p, v: (key_transform(p), v))
    return TreeStream.rebuild(transformed)
