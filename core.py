import sys
from typing import Any, Callable, Dict, Tuple


class MemoizedSlotRegistry(type):
    """Metaclass providing slot-cached method routing for core execution."""
    def __new__(mcs, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]):
        slots = list(attrs.get('__slots__', ()))
        slots.extend(['_route_cache', '_intern_table'])
        attrs['__slots__'] = tuple(set(slots))
        return super().__new__(mcs, name, bases, attrs)


class CoreExecutionEngine(metaclass=MemoizedSlotRegistry):
    """High-throughput command processor using string interning and bit-hashed routing."""
    __slots__ = ('_registry',)

    def __init__(self) -> None:
        self._registry: Dict[int, Callable[..., Any]] = {}
        self._route_cache: Dict[Tuple[Any, ...], Any] = {}
        self._intern_table: Dict[str, int] = {}

    def register_route(self, path: str) -> Callable:
        interned_path = sys.intern(path)
        path_hash = hash(interned_path)

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._intern_table[path] = path_hash
            self._registry[path_hash] = fn
            return fn
        return decorator

    def execute(self, path: str, *args: Any, **kwargs: Any) -> Any:
        path_hash = self._intern_table.get(path)
        if path_hash is None:
            path_hash = hash(sys.intern(path))

        handler = self._registry.get(path_hash)
        if not handler:
            raise RuntimeError(f"Unresolved core path: {path}")

        cache_key = (path_hash, args, tuple(sorted(kwargs.items())))
        if cache_key in self._route_cache:
            return self._route_cache[cache_key]

        result = handler(*args, **kwargs)
        if len(self._route_cache) < 2048:
            self._route_cache[cache_key] = result
        return result

    def flush_cache(self) -> None:
        self._route_cache.clear()
