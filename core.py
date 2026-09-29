from typing import Any, Callable


class DataStream:
    """Creative pipeline wrapper for flexible dictionary and list transformations."""

    def __init__(self, data: Any):
        self._data = data

    @property
    def value(self) -> Any:
        return self._data

    def __or__(self, func: Callable[[Any], Any]) -> "DataStream":
        """Pipe data into a transforming function or item-wise map."""
        if isinstance(self._data, list) and not getattr(func, "__is_aggregate__", False):
            return DataStream([func(item) for item in self._data])
        return DataStream(func(self._data))

    def __matmul__(self, path: str) -> "DataStream":
        """Extract nested key or index using @ syntax ('user.profile.id')."""
        current = self._data
        for key in path.split("."):
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, (list, tuple)) and key.isdigit():
                idx = int(key)
                current = current[idx] if 0 <= idx < len(current) else None
            else:
                current = None
            if current is None:
                break
        return DataStream(current)

    def __repr__(self) -> str:
        return f"DataStream({repr(self._data)})"


def flatten_keys(data: dict, prefix: str = "", sep: str = ".") -> dict:
    """Recursively flatten nested dictionary keys."""
    items = []
    for k, v in data.items():
        new_key = f"{prefix}{sep}{k}" if prefix else str(k)
        if isinstance(v, dict):
            items.extend(flatten_keys(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
