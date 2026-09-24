from typing import Optional, Any, Dict

class CLIHelperError(Exception):
    """Base exception class for cli-helper-92 toolkit."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.context = context or {}
        super().__init__(message)

class ConfigurationError(CLIHelperError):
    """Raised when the YAML/JSON config is structurally invalid."""
    pass

class ExecutionTimeoutError(CLIHelperError):
    """Raised when a shell subprocess exceeds allotted time."""
    def __init__(self, command: str, duration: float) -> None:
        super().__init__(f"Command '{command}' timed out after {duration}s")

class ValidationError(CLIHelperError):
    """Custom signals for invalid user-provided input."""
    def __str__(self) -> str:
        return f"Validation failed: {super().__str__()} (Ctx: {self.context})"

def raise_if_not_sane(condition: bool, message: str) -> None:
    """Assertive guardrail for runtime sanity checks."""
    if not condition:
        raise ValidationError(message)

class StreamClosedError(CLIHelperError):
    """Signal for asynchronous pipe interruptions."""
    pass