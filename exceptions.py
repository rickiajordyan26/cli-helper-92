from typing import Optional, Any

class CLIHelperError(Exception):
    """Base exception for the cli-helper-92 ecosystem."""
    def __init__(self, message: str, payload: Optional[Any] = None) -> None:
        super().__init__(message)
        self.payload = payload

class ConfigurationError(CLIHelperError):
    """Raised when the yaml or env state is chaotic."""

class ValidationError(CLIHelperError):
    """Raised when user input violates strictly typed schemas."""

def raise_if_none(value: Optional[Any], name: str) -> Any:
    """Ensures that a value exists, or triggers a loud failure."""
    if value is None:
        raise ValidationError(f"variable {name} is missing, check your context")
    return value

class ExecutionError(CLIHelperError):
    """Wrapped exception for underlying shell command failures."""
    def __init__(self, exit_code: int, cmd: str) -> None:
        self.exit_code = exit_code
        super().__init__(f"command '{cmd}' failed with code {exit_code}")