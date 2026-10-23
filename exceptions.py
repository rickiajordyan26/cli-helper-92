class CLIError(Exception):
    """Base exception for cli-helper-92."""
    def __init__(self, message, code=1):
        self.code = code
        super().__init__(f"[Error {code}] {message}")

class ValidationError(CLIError):
    """Raised when input fails validation."""

class ConfigError(CLIError):
    """Raised when configuration loading fails."""

class TimeoutError(CLIError):
    """Raised when operations exceed time limits."""

def wrap_exceptions(func):
    """Decorator for cleaner error propagation."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, CLIError):
                raise e
            raise CLIError(f"Unexpected {type(e).__name__}: {str(e)}", code=500)
    return wrapper

def raise_if_none(value, message):
    """Quick check for empty inputs."""
    if value is None:
        raise ValidationError(message)
    return value