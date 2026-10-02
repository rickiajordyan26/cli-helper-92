from difflib import get_close_matches
from typing import Any, Union


class FluentData:
    """Wrapper for dicts/lists allowing division-based path traversal and fuzzy key matching."""

    def __init__(self, data: Any):
        self._data = data._data if isinstance(data, FluentData) else data

    def __truediv__(self, key: Union[str, int]) -> "FluentData":
        """Traverse nested structures using the '/' operator with fallback fuzzy matching."""
        if isinstance(self._data, dict):
            if key in self._data:
                return FluentData(self._data[key])

            if isinstance(key, str):
                string_keys = [k for k in self._data.keys() if isinstance(k, str)]
                matches = get_close_matches(key, string_keys, n=1, cutoff=0.5)
                if matches:
                    return FluentData(self._data[matches[0]])

            raise KeyError(f"Key '{key}' not found (even with fuzzy matching)")

        if isinstance(self._data, (list, tuple)):
            try:
                return FluentData(self._data[int(key)])
            except (ValueError, IndexError):
                raise IndexError(f"Invalid index or path segment '{key}'")

        raise TypeError(f"Cannot traverse leaf node of type {type(self._data).__name__}")

    def unwrap(self) -> Any:
        """Return the unwrapped Python data structure."""
        return self._data

    def __repr__(self) -> str:
        return f"FluentData({self._data!r})"


def fluid(data: Any) -> FluentData:
    """Entrypoint to wrap dictionary/list into FluentData."""
    return FluentData(data)
