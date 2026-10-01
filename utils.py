import functools
from typing import Any, Callable, Iterable, TypeVar, Dict

T = TypeVar('T')

class DataPipeline:
    """A whimsical data processing chain using functional currying."""
    def __init__(self, data: Any):
        self._data = data

    def apply(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        self._data = func(self._data)
        return self

    def result(self) -> Any:
        return self._data

def compose(*funcs: Callable) -> Callable:
    """Functional pipe composition for data transformation."""
    return lambda x: functools.reduce(lambda acc, f: f(acc), funcs, x)

def deep_extract(obj: Dict, path: str, default: Any = None) -> Any:
    """Recursive key retrieval with dot-notation support."""
    keys = path.split('.')
    for key in keys:
        if isinstance(obj, dict): 
            obj = obj.get(key, default)
        else:
            return default
    return obj

def batch_process(items: Iterable[T], size: int) -> Iterable[list[T]]:
    """Memory-efficient batching of data chunks."""
    it = iter(items)
    while True:
        batch = []
        try:
            for _ in range(size):
                batch.append(next(it))
            yield batch
        except StopIteration:
            if batch: yield batch
            break