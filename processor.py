import collections
from typing import Any, Iterable, Dict, Union

class DataTransformer:
    def __init__(self, data: Any):
        self.data = data

    def flatten(self) -> list:
        items = []
        queue = collections.deque([self.data])
        while queue:
            curr = queue.popleft()
            if isinstance(curr, (list, tuple)):
                queue.extendleft(reversed(curr))
            else:
                items.append(curr)
        return items

    def structure(self, keys: Iterable[str]) -> Dict[str, Any]:
        values = self.flatten()
        return {k: (values[i] if i < len(values) else None) for i, k in enumerate(keys)}

    def mask(self, target_keys: Iterable[str], replacement: str = '***') -> Union[dict, list]:
        if isinstance(self.data, dict):
            return {k: (replacement if k in target_keys else v) for k, v in self.data.items()}
        if isinstance(self.data, list):
            return [self._mask_item(item, target_keys, replacement) for item in self.data]
        return self.data

    def _mask_item(self, item, keys, rep):
        return {k: (rep if k in keys else v) for k, v in item.items()} if isinstance(item, dict) else item

def process_data(data: Any) -> DataTransformer:
    return DataTransformer(data)