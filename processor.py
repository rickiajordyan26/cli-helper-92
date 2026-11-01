import re
from typing import Any, Callable, Union


class DataWeaver:
    """A creative fluid wrapper for querying and morphing nested collections."""

    def __init__(self, payload: Any):
        self.data = payload

    def __or__(self, transform: Callable[[Any], Any]) -> "DataWeaver":
        """Use bitwise OR as a pipeline operator."""
        if callable(transform):
            return DataWeaver(transform(self.data))
        return self

    def pluck(self, *path: Union[str, int]) -> "DataWeaver":
        """Deeply extract nested elements using path segments or regex patterns."""
        curr = self.data
        for key in path:
            if isinstance(curr, dict) and isinstance(key, str):
                if key in curr:
                    curr = curr[key]
                else:
                    matched = [v for k, v in curr.items() if re.search(str(key), str(k))]
                    curr = matched if matched else None
            elif isinstance(curr, (list, tuple)) and isinstance(key, int):
                curr = curr[key] if 0 <= key < len(curr) else None
            else:
                curr = None
            if curr is None:
                break
        return DataWeaver(curr)

    def flatten(self) -> "DataWeaver":
        """Flatten arbitrarily nested dictionaries and lists into key-value tuples."""
        def _unravel(obj, prefix=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{prefix}.{k}" if prefix else str(k)
                    yield from _unravel(v, new_key)
            elif isinstance(obj, (list, tuple)):
                for idx, v in enumerate(obj):
                    yield from _unravel(v, f"{prefix}[{idx}]")
            else:
                yield (prefix, obj)

        return DataWeaver(dict(_unravel(self.data)))

    def unwrap(self) -> Any:
        """Extract the underlying processed payload."""
        return self.data


def process_nested_data(data: Any, path: str = "", flatten: bool = False) -> Any:
    """Helper utility for fluid extraction and flattening of generic data."""
    weaver = DataWeaver(data)
    if path:
        segments = [int(s) if s.isdigit() else s for s in path.split(".")]
        weaver = weaver.pluck(*segments)
    if flatten:
        weaver = weaver.flatten()
    return weaver.unwrap()
