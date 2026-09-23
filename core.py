import time
from typing import Callable, Any, Dict, Tuple

class FastCoreEngine:
    """Optimized execution core using slots, bytecode hash keys, and fast-path memoization."""
    __slots__ = ('_registry', '_cache', '_max_cache', '_stats')

    def __init__(self, max_cache: int = 256):
        self._registry: Dict[str, Callable[..., Any]] = {}
        self._cache: Dict[int, Any] = {}
        self._max_cache = max_cache
        self._stats = {"hits": 0, "misses": 0, "exec_time_ns": 0}

    def register(self, command: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._registry[command.strip().lower()] = func
            return func
        return decorator

    def dispatch(self, raw_input: str, *args, **kwargs) -> Any:
        t0 = time.perf_counter_ns()
        input_key = hash((raw_input, args, tuple(sorted(kwargs.items()))))

        if input_key in self._cache:
            self._stats["hits"] += 1
            self._stats["exec_time_ns"] += time.perf_counter_ns() - t0
            return self._cache[input_key]

        self._stats["misses"] += 1
        tokens = raw_input.strip().split()
        cmd_name = tokens[0].lower() if tokens else ""
        
        if cmd_name not in self._registry:
            raise KeyError(f"Unregistered CLI command execution attempt: '{cmd_name}'")

        result = self._registry[cmd_name](*args, **kwargs)

        if len(self._cache) >= self._max_cache:
            self._cache.pop(next(iter(self._cache)))

        self._cache[input_key] = result
        self._stats["exec_time_ns"] += time.perf_counter_ns() - t0
        return result

    def metrics(self) -> Dict[str, Any]:
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total) if total > 0 else 0.0
        return {
            "total_calls": total,
            "hit_rate_pct": round(hit_rate * 100, 2),
            "avg_ns": self._stats["exec_time_ns"] // (total or 1)
        }
