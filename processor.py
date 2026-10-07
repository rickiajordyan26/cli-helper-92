import functools
import itertools
from typing import Any, Callable, Dict, List

class DataStreamProcessor:
    def __init__(self, pipeline: List[Callable[[Any], Any]] = None):
        self._pipeline = pipeline or []
        self._buffer: List[Any] = []

    def ingest(self, item: Any) -> None:
        self._buffer.append(item)

    def process_all(self) -> List[Any]:
        results = []
        for item in self._buffer:
            transformed = functools.reduce(lambda acc, f: f(acc), self._pipeline, item)
            results.append(transformed)
        return results

    def batch_process(self, chunk_size: int) -> List[List[Any]]:
        args = [iter(self._buffer)] * chunk_size
        return [list(filter(None, batch)) for batch in zip(*args)]

    def clear(self) -> None:
        self._buffer.clear()

def chain_operations(*funcs: Callable) -> Callable:
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)

if __name__ == '__main__':
    processor = DataStreamProcessor(pipeline=[lambda x: x * 2, lambda x: x + 10])
    [processor.ingest(i) for i in range(5)]
    print(processor.process_all())