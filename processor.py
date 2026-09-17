import json
from typing import Any, Callable, Dict, Union

class DataTransformer:
    def __init__(self, pipeline: list = None):
        self.pipeline = pipeline or []

    def register(self, func: Callable[[Any], Any]):
        self.pipeline.append(func)
        return self

    def process(self, data: Any) -> Any:
        for step in self.pipeline:
            data = step(data)
        return data

    @staticmethod
    def safe_json(data: Any) -> str:
        try:
            return json.dumps(data, indent=2)
        except (TypeError, ValueError):
            return '{"error": "serialization failed"}'

def clean_string(data: Any) -> str:
    return str(data).strip().lower()

def ensure_list(data: Any) -> list:
    return [data] if not isinstance(data, list) else data

def batch_processor(data_list: list, transform_func: Callable) -> list:
    return [transform_func(item) for item in data_list]

# Dynamic dispatch approach to object handling
class FlexibleHandler:
    def __init__(self, registry: Dict[type, Callable] = None):
        self._registry = registry or {}

    def handle(self, item: Any) -> Any:
        handler = self._registry.get(type(item), lambda x: x)
        return handler(item)

    def update_map(self, type_key: type, handler: Callable):
        self._registry[type_key] = handler