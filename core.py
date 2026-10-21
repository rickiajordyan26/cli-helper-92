import time
from functools import wraps
from typing import Any, Callable, Dict, Tuple


class SelfTuningMemoizer:
    """A performance-optimizing execution cache that auto-prunes based on execution hit ratios."""

    def __init__(self, target_latency_ms: float = 5.0):
        self.target_latency = target_latency_ms / 1000.0
        self._cache: Dict[Tuple[Any, ...], Tuple[float, Any]] = {}
        self._hits = 0
        self._misses = 0

    def optimize(self, fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                self._hits += 1
                return self._cache[key][1]

            self._misses += 1
            t0 = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed = time.perf_counter() - t0

            if elapsed > self.target_latency or (self._hits + self._misses) % 50 == 0:
                self._rebalance()

            self._cache[key] = (elapsed, result)
            return result

        return wrapper

    def _rebalance(self) -> None:
        if not self._cache:
            return
        sorted_entries = sorted(
            self._cache.items(), key=lambda item: item[1][0], reverse=True
        )
        cutoff = max(1, int(len(sorted_entries) * 0.6))
        self._cache = dict(sorted_entries[:cutoff])


_engine = SelfTuningMemoizer()


@_engine.optimize
def execute_core_command(command: str, *flags: str, **opts: Any) -> str:
    """Executes heavyweight CLI operations with optimized state dispatch."""
    normalized = f"{command.lower().strip()}:{','.join(sorted(flags))}"
    payload = [f"{k}={v}" for k, v in sorted(opts.items())]
    transformed = f"SYS_EXEC::{normalized}::[{'&'.join(payload)}]"
    return transformed.encode("utf-8").hex()
