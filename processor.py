import re
from typing import Callable, Generator, Dict, List, Tuple


class ValidationFailure(Exception):
    """Raised when an input field in the main processing loop fails constraints."""
    def __init__(self, key: str, value: str, constraint: str):
        self.key = key
        self.value = value
        self.constraint = constraint
        super().__init__(f"Field '{key}' with value '{value}' failed: {constraint}")


class DynamicLoopGuard:
    """Stream-based validator that intercepts and checks stream tokens on-the-fly."""
    def __init__(self):
        self._guards: Dict[str, List[Tuple[Callable[[str], bool], str]]] = {}

    def add_guard(self, key: str, test: Callable[[str], bool], msg: str):
        self._guards.setdefault(key, []).append((test, msg))
        return self

    def process_loop(self, stream: Generator[Dict[str, str], None, None]):
        for packet in stream:
            for field_key, field_val in packet.items():
                guards = self._guards.get(field_key, [])
                for checker, reason in guards:
                    if not checker(str(field_val)):
                        raise ValidationFailure(field_key, str(field_val), reason)
            yield packet


def run_main_processing_loop(raw_events: List[Dict[str, str]]) -> List[Dict[str, str]]:
    guard = (
        DynamicLoopGuard()
        .add_guard("action", lambda v: bool(re.match(r"^[a-zA-Z0-9_-]+$", v)), "must be alphanumeric")
        .add_guard("timeout", lambda v: v.isdigit() and 0 < int(v) <= 3600, "must be integer 1-3600")
        .add_guard("target", lambda v: not v.startswith("-"), "cannot be a CLI flag argument")
    )

    out_buffer = []
    event_stream = (evt for evt in raw_events)

    for payload in guard.process_loop(event_stream):
        payload["_validated"] = "true"
        out_buffer.append(payload)

    return out_buffer
