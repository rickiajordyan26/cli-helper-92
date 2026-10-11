import json
from typing import Any, Callable, Dict, List, Union


class DataPipe:
    """An operator-overloaded pipe wrapper for CLI data manipulation."""

    def __init__(self, data: Any = None):
        self.data = data

    def __ror__(self, other: Any) -> "DataPipe":
        return DataPipe(other)

    def __or__(self, func: Callable[[Any], Any]) -> "DataPipe":
        if callable(func):
            return DataPipe(func(self.data))
        raise TypeError(f"Operand must be callable, got {type(func).__name__}")

    def __rshift__(self, format_type: str) -> str:
        """Format data for terminal presentation using '>>' operator."""
        if format_type == "json":
            return json.dumps(self.data, indent=2, default=str)
        elif format_type == "kv":
            if isinstance(self.data, dict):
                return "\n".join(f"{k} = {v}" for k, v in self.data.items())
            return str(self.data)
        elif format_type == "csv" and isinstance(self.data, list) and self.data:
            if isinstance(self.data[0], dict):
                headers = list(self.data[0].keys())
                rows = [",".join(headers)]
                for item in self.data:
                    rows.append(",".join(str(item.get(h, "")) for h in headers))
                return "\n".join(rows)
        return str(self.data)

    def __repr__(self) -> str:
        return f"DataPipe({repr(self.data)})"


def pluck(*keys: str) -> Callable[[Union[Dict, List[Dict]]], Any]:
    """Extract specified keys from a dict or list of dicts."""
    def _pluck(data: Any) -> Any:
        if isinstance(data, dict):
            return {k: data[k] for k in keys if k in data}
        if isinstance(data, list):
            return [{k: item[k] for k in keys if k in item} for item in data if isinstance(item, dict)]
        return data
    return _pluck


def flatten_dict(sep: str = ".") -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Transform nested dictionary into a single-level dictionary."""
    def _flatten(data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            return {}
        out: Dict[str, Any] = {}
        def _rec(curr: Any, prefix: str):
            if isinstance(curr, dict):
                for k, v in curr.items():
                    _rec(v, f"{prefix}{sep}{k}" if prefix else k)
            else:
                out[prefix] = curr
        _rec(data, "")
        return out
    return _flatten
