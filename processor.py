import sys
from typing import Generator, Dict, Any, Callable, List, Tuple

class InputValidatorPipeline:
    """Creative input validator pipeline using operator chaining for loop processing."""

    def __init__(self):
        self.validators: List[Tuple[str, Callable[[str], bool], str]] = [
            ("length_check", lambda s: 0 < len(s.strip()) <= 256, "Input exceeds maximum length (256 chars)"),
            ("sanitation", lambda s: not any(c in s for c in [";", "&&", "||", "`"]), "Forbidden injection characters detected"),
            ("structure", lambda s: bool(s.strip().split()), "Input cannot be empty or whitespace only"),
        ]

    def validate(self, raw: str) -> Dict[str, Any]:
        cleaned = raw.strip()
        for name, check, error_msg in self.validators:
            if not check(cleaned):
                return {"is_valid": False, "error": f"[{name}] {error_msg}", "data": None}
        
        parts = cleaned.split()
        return {
            "is_valid": True,
            "error": None,
            "data": {"cmd": parts[0].lower(), "args": parts[1:], "raw": cleaned}
        }

class LoopProcessor:
    def __init__(self):
        self.pipeline = InputValidatorPipeline()

    def run_loop(self, stream: List[str]) -> Generator[str, None, None]:
        """Process stream items through validation pipeline."""
        for idx, raw_input in enumerate(stream, start=1):
            result = self.pipeline.validate(raw_input)
            if not result["is_valid"]:
                yield f"Line {idx} Error: {result['error']}"
                continue

            payload = result["data"]
            if payload["cmd"] in ("exit", "quit"):
                yield f"Line {idx}: Termination requested."
                break

            yield f"Line {idx} Processed: command='{payload['cmd']}', args={payload['args']}"
