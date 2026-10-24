import sys
from typing import Optional, Dict, Any

class CLIHelperError(Exception):
    """Base exception with interactive CLI formatting capabilities."""
    code: int = 1
    prefix: str = "[ERROR]"

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}

    def format_cli(self, use_color: bool = True) -> str:
        if not use_color or not sys.stdout.isatty():
            ctx_str = f" | context={self.context}" if self.context else ""
            return f"{self.prefix} {self.message}{ctx_str}"
        
        red_bold = "\033[1;31m"
        dim = "\033[2m"
        reset = "\033[0m"
        ctx_str = f" {dim}({self.context}){reset}" if self.context else ""
        return f"{red_bold}{self.prefix}{reset} {self.message}{ctx_str}"


class ConfigurationError(CLIHelperError):
    code = 2
    prefix = "[CONFIG_ERR]"


class ExecutionError(CLIHelperError):
    code = 3
    prefix = "[EXEC_ERR]"


class ValidationError(CLIHelperError):
    code = 4
    prefix = "[VALID_ERR]"


def error_chain(*exceptions: CLIHelperError) -> CLIHelperError:
    """Flattens multiple CLI errors into a single aggregated exception."""
    messages = [e.format_cli() for e in exceptions]
    combined = "Multi-error cascade:\n  - " + "\n  - ".join(messages)
    first_code = exceptions[0].code if exceptions else 1
    err = CLIHelperError(combined)
    err.code = first_code
    return err
