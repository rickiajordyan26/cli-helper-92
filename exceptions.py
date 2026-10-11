class CLIError(Exception):
    """Base exception for cli-helper-92 operations."""
    def __init__(self, message, code=1):
        self.code = code
        super().__init__(f"[{code}] {message}")

class ConfigError(CLIError):
    """Raised when configuration loading fails."""
    pass

class ValidationError(CLIError):
    """Raised when input validation fails."""
    pass

def raise_if(condition, message, exception_cls=CLIError, code=400):
    """Conditional exception raiser for fluid control flow."""
    if condition:
        raise exception_cls(message, code)

def catch_or_default(func, default=None):
    """Decorator pattern for safe execution of operations."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CLIError:
            return default
    return wrapper

class ExceptionReporter:
    """Centralized diagnostic tool for session tracebacks."""
    @staticmethod
    def format(exc: Exception) -> str:
        return f"!! {exc.__class__.__name__}: {str(exc)}"