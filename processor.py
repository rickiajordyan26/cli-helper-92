import sys
from typing import Dict, List, Tuple


class ChunkProcessor:
    """Memoryview-optimized stream chunk processor for fast CLI pipe parsing."""

    __slots__ = (
        "_buffer",
        "_view_buffer",
        "_capacity",
        "_head",
        "_tail",
        "_token_cache",
    )

    def __init__(self, capacity: int = 1024 * 1024) -> None:
        self._capacity = capacity
        self._buffer = bytearray(capacity)
        self._view_buffer = memoryview(self._buffer)
        self._head = 0
        self._tail = 0
        self._token_cache: Dict[int, Tuple[int, ...]] = {}

    def push(self, data: bytes) -> int:
        data_len = len(data)
        if self._tail + data_len > self._capacity:
            self._compact()

        available = self._capacity - self._tail
        write_size = min(data_len, available)
        self._buffer[self._tail : self._tail + write_size] = data[:write_size]
        self._tail += write_size
        return write_size

    def _compact(self) -> None:
        if self._head == 0:
            return
        remaining = self._tail - self._head
        if remaining > 0:
            self._buffer[0:remaining] = self._buffer[self._head : self._tail]
        self._head = 0
        self._tail = remaining

    def fast_tokenize(self, sep: int = 10) -> List[bytes]:
        active_slice = self._view_buffer[self._head : self._tail]
        lines: List[bytes] = []
        last_pos = 0

        for i, byte in enumerate(active_slice):
            if byte == sep:
                lines.append(active_slice[last_pos:i].tobytes())
                last_pos = i + 1

        self._head += last_pos
        return lines

    def drain(self) -> bytes:
        remaining = self._view_buffer[self._head : self._tail].tobytes()
        self._head = 0
        self._tail = 0
        return remaining
