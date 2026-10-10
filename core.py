from typing import Any, Callable, Dict, Union


class DataTransformer:
    """A fluent wrapper around nested dict/list data with pipeable transformations."""

    def __init__(self, data: Any):
        self.data = data

    def select(self, *keys: Union[str, int]) -> "DataTransformer":
        """Navigate deeply nested data structures using keys or indices."""
        curr = self.data
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            elif isinstance(curr, (list, tuple)) and isinstance(k, int) and 0 <= k < len(curr):
                curr = curr[k]
            else:
                curr = None
                break
        return DataTransformer(curr)

    def map_deep(self, fn: Callable[[Any], Any]) -> "DataTransformer":
        """Recursively apply a function to all scalar values in the structure."""
        def _transform(val):
            if isinstance(val, dict):
                return {k: _transform(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [_transform(v) for v in val]
            elif isinstance(val, tuple):
                return tuple(_transform(v) for v in val)
            return fn(val)

        return DataTransformer(_transform(self.data))

    def flatten(self, sep: str = ".") -> Dict[str, Any]:
        """Flatten nested dictionary into a single-level dict with delimited keys."""
        out = {}

        def _flatten(val, prefix=""):
            if isinstance(val, dict):
                for k, v in val.items():
                    new_key = f"{prefix}{sep}{k}" if prefix else str(k)
                    _flatten(v, new_key)
            elif isinstance(val, (list, tuple)):
                for idx, item in enumerate(val):
                    new_key = f"{prefix}{sep}{idx}" if prefix else str(idx)
                    _flatten(item, new_key)
            else:
                out[prefix] = val

        _flatten(self.data)
        return out

    def __or__(self, func: Callable[["DataTransformer"], Any]) -> Any:
        """Pipe operator support for transformation functions."""
        return func(self)

    def unwrap(self) -> Any:
        return self.data


def process_data(data: Any) -> DataTransformer:
    return DataTransformer(data)
