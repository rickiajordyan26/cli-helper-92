import re
from typing import Any, Callable, Dict, Union

def create_pipeline(funcs: list[Callable]) -> Callable:
    """Compose list of functions into a data pipeline."""
    def pipeline(data: Any) -> Any:
        for f in funcs:
            data = f(data)
        return data
    return pipeline

def sanitizer(pattern: str) -> Callable:
    """Factory for regex-based string cleaning."""
    rx = re.compile(pattern)
    return lambda x: rx.sub('', str(x))

def type_enforcer(target_type: type) -> Callable:
    """Casting wrapper for data structure normalization."""
    return lambda x: target_type(x) if not isinstance(x, target_type) else x

def validation_gate(condition: Callable, error_msg: str) -> Callable:
    """Conditional execution block for data flow."""
    def gate(data: Any) -> Any:
        if not condition(data):
            raise ValueError(error_msg)
        return data
    return gate

def map_schema(schema: Dict[str, Callable], data: dict) -> dict:
    """Transformation of dict values via mapping functions."""
    return {k: schema[k](v) for k, v in data.items() if k in schema}
