from typing import Any, Union, Dict, List

class FuzzyDataWeaver:
    """
    A creative data-handling wrapper that allows nested path retrieval using 
    the division (/) operator and deep-merging using the bitwise OR (|) operator.
    """
    def __init__(self, data: Any):
        self.data = data

    def __truediv__(self, path: str) -> Any:
        """
        Traverse nested dictionaries and lists using slash-separated paths.
        Example: weaver / 'metadata/users/0/name'
        """
        if not isinstance(path, str) or not path:
            return self

        parts = [int(p) if p.isdigit() else p for p in path.strip('/').split('/')]
        current = self.data

        for part in parts:
            try:
                if isinstance(current, list) and isinstance(part, int):
                    current = current[part]
                elif isinstance(current, dict):
                    current = current[part]
                else: 
                    return None
            except (IndexError, KeyError, TypeError, ValueError):
                return None

        if isinstance(current, (dict, list)):
            return FuzzyDataWeaver(current)
        return current

    def __or__(self, other: "FuzzyDataWeaver") -> "FuzzyDataWeaver":
        """Deep-merges two structures, aligning lists index-wise if overlapping."""
        if not isinstance(other, FuzzyDataWeaver):
            return self
        return FuzzyDataWeaver(self._deep_merge(self.data, other.data))

    def _deep_merge(self, left: Any, right: Any) -> Any:
        if isinstance(left, dict) and isinstance(right, dict):
            merged = dict(left)
            for key, val in right.items():
                if key in merged:
                    merged[key] = self._deep_merge(merged[key], val)
                else:
                    merged[key] = val
            return merged
        
        if isinstance(left, list) and isinstance(right, list):
            merged_list = []
            for i in range(max(len(left), len(right))):
                if i < len(left) and i < len(right):
                    merged_list.append(self._deep_merge(left[i], right[i]))
                elif i < len(left):
                    merged_list.append(left[i])
                else:
                    merged_list.append(right[i])
            return merged_list

        return right if right is not None else left

    def unwrap(self) -> Any:
        """Returns the raw underlying data structure."""
        return self.data
