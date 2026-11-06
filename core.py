import functools
import sys
from typing import Any, Callable, Dict, Tuple


class OptimizedDispatcher:
    """Fast dynamic command dispatch engine using interned string caches."""

    __slots__ = ("_registry", "_cache", "_hits", "_misses")

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., Any]] = {}
        self._cache: Dict[Tuple[str, Tuple[Any, ...]], Any] = {}
        self._hits: int = 0
        self._misses: int = 0

    def register(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._registry[sys.intern(name)] = func
            return func

        return decorator

    @functools.lru_cache(maxsize=2048)
    def _tokenize(self, raw_cmd: str) -> Tuple[str, ...]:
        return tuple(sys.intern(token) for token in raw_cmd.strip().split())

    def dispatch(self, raw_input: str, *extra_args: Any) -> Any:
        tokens = self._tokenize(raw_input)
        if not tokens:
            return None

        cmd, args = tokens[0], tokens[1:] + extra_args
        cache_key = (cmd, args)

        if cache_key in self._cache:
            self._hits += 1
            return self._cache[cache_key]

        self._misses += 1
        handler = self._registry.get(cmd)
        if not handler:
            raise KeyError(f"Command '{cmd}' not found in runtime registry")

        res = handler(*args)
        self._cache[cache_key] = res
        return res

    def get_stats(self) -> Dict[str, int]:
        return {"hits": self._hits, "misses": self._misses, "cache_size": len(self._cache)}

    def flush(self) -> None:
        self._cache.clear()
        self._tokenize.cache_clear()
        self._hits = 0
        self._misses = 0
