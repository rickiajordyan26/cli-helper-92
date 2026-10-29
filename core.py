import sys
from typing import Any, Callable, Dict, Tuple

class FastCoreBuffer:
    __slots__ = ('_pool', '_capacity', '_active_index')

    def __init__(self, capacity: int = 1024 * 64):
        self._capacity = capacity
        self._pool = bytearray(capacity)
        self._active_index = 0

    def write(self, data: bytes) -> memoryview:
        length = len(data)
        if self._active_index + length > self._capacity:
            self._active_index = 0
        start = self._active_index
        self._pool[start:start + length] = data
        self._active_index += length
        return memoryview(self._pool)[start:start + length]

class OptimizedDispatcher:
    __slots__ = ('_registry', '_memo', '_hits')

    def __init__(self):
        self._registry: Dict[int, Callable[..., Any]] = {}
        self._memo: Dict[Tuple[int, int], Any] = {}
        self._hits: int = 0

    @staticmethod
    def _fnv1a_hash(key: str) -> int:
        h = 0x811c9dc5
        for byte in key.encode('utf-8'):
            h = ((h ^ byte) * 0x01000193) & 0xFFFFFFFF
        return h

    def register(self, command: str, func: Callable[..., Any]) -> None:
        cmd_hash = self._fnv1a_hash(command)
        self._registry[cmd_hash] = func

    def execute(self, command: str, payload: str = "") -> Any:
        cmd_hash = self._fnv1a_hash(command)
        arg_hash = self._fnv1a_hash(payload)
        cache_key = (cmd_hash, arg_hash)

        if cache_key in self._memo:
            self._hits += 1
            return self._memo[cache_key]

        handler = self._registry.get(cmd_hash)
        if not handler:
            raise KeyError(f"Unknown CLI command token: {command}")

        result = handler(payload)
        if len(self._memo) < 512:
            self._memo[cache_key] = result
        return result

buffer_pool = FastCoreBuffer()
dispatcher = OptimizedDispatcher()
