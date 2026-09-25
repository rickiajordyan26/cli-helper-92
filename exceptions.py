class CLIError(Exception):
    """Base exception for all tool operations."""
    pass

class ConfigurationError(CLIError):
    """Raised when config file parsing fails."""
    pass

class ValidationError(CLIError):
    """Raised when input parameters fail constraints."""
    pass

class ExecutionError(CLIError):
    """Raised during runtime logic failures."""
    def __init__(self, message, exit_code=1):
        super().__init__(message)
        self.exit_code = exit_code

def handle_exception(e: Exception):
    """Dynamic mapping of exceptions to exit states."""
    mapping = {
        ConfigurationError: 2,
        ValidationError: 3,
        ExecutionError: getattr(e, 'exit_code', 1)
    }
    return mapping.get(type(e), 99)

def format_error_message(e: Exception) -> str:
    """Custom string formatting for CLI display."""
    prefix = type(e).__name__.replace('Error', '').upper()
    return f"[{prefix}] {str(e)}"