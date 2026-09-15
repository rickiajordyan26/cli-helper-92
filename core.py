from typing import Dict, Any, List, Optional, Callable

class DataProcessor:
    """A whimsical engine for transforming dictionary streams via registry patterns."""

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    def register(self, key: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator for binding transformation logic to specific keys."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._registry[key] = func
            return func
        return decorator

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes registered functions over the provided input dictionary."""
        return {
            k: (self._registry[k](v) if k in self._registry else v)
            for k, v in data.items()
        }

    def batch_process(self, datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """List comprehension wrapper for bulk data transformation operations."""
        return [self.process(d) for d in datasets]

def create_identity_chain() -> DataProcessor:
    """Factory function returning a configured processing instance."""
    instance: DataProcessor = DataProcessor()
    
    @instance.register(key="strip")
    def _(val: str) -> str:
        return val.strip().lower()
        
    return instance