from typing import Callable, Any, Dict, List, Optional

class StreamHandler:
    """Orchestrates data flow using a chain of functional transformations."""

    def __init__(self, pipeline: List[Callable[[Any], Any]]) -> None:
        self.pipeline: List[Callable[[Any], Any]] = pipeline

    def process(self, data: Any) -> Any:
        """Executes sequential processing through the pipeline stack."""
        for step in self.pipeline:
            data = step(data)
        return data

def compose_flow(base_value: Dict[str, Any], mods: List[Callable[[Dict[str, Any]], Dict[str, Any]]]) -> Dict[str, Any]:
    """Applies a series of functional mutations to a base dictionary."""
    for mod in mods:
        base_value = mod(base_value)
    return base_value

if __name__ == '__main__':
    # Example usage: transforming configuration dictionary
    def add_meta(d: Dict[str, Any]) -> Dict[str, Any]:
        d.update({"processed": True})
        return d

    def clean_nulls(d: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in d.items() if v is not None}

    handler = StreamHandler([add_meta, clean_nulls])
    result = handler.process({"a": 1, "b": None})
    print(result)