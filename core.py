import functools
import hashlib
import time
from typing import Any, Callable, Dict, List, Tuple


class CachedExecutionEngine:
    """Fast dynamic command execution engine with bytecode signature memoization."""

    def __init__(self, capacity: int = 256):
        self._capacity = capacity
        self._registry: Dict[bytes, Tuple[float, Any]] = {}
        self._hits = 0
        self._misses = 0

    def _hash_payload(self, command: str, *args: Any, **kwargs: Any) -> bytes:
        payload = f"{command}:{args}:{sorted(kwargs.items())}".encode("utf-8")
        return hashlib.blake2b(payload, digest_size=16).digest()

    def execute(self, func: Callable[..., Any], command: str, *args: Any, **kwargs: Any) -> Any:
        sig = self._hash_payload(command, *args, **kwargs)
        now = time.monotonic()

        if sig in self._registry:
            _, result = self._registry[sig]
            self._registry[sig] = (now, result)
            self._hits += 1
            return result

        self._misses += 1
        result = func(command, *args, **kwargs)

        if len(self._registry) >= self._capacity:
            oldest_key = min(self._registry, key=lambda k: self._registry[k][0])
            del self._registry[oldest_key]

        self._registry[sig] = (now, result)
        return result

    @property
    def efficiency_ratio(self) -> float:
        total = self._hits + self._misses
        return (self._hits / total) if total > 0 else 0.0


_engine_instance = CachedExecutionEngine()


def memoized_runner(command_str: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Core command pipeline transformer and execution wrapper."""
    def _parse_and_transform(cmd: str, *a: Any, **kw: Any) -> Dict[str, Any]:
        tokens = [t.strip() for t in cmd.split() if t.strip()]
        parsed_flags = {k: v for k, v in kw.items()}
        return {
            "raw": cmd,
            "executable": tokens[0] if tokens else "",
            "flags": tokens[1:] + list(a),
            "kwargs": parsed_flags,
            "timestamp": time.time_ns(),
        }

    return _engine_instance.execute(_parse_and_transform, command_str, *args, **kwargs)
