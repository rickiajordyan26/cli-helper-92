"""Structured exception handling module with CLI context dynamic wrapping."""

import sys
from typing import Any, Dict, Optional, Type, TypeVar

E = TypeVar("E", bound="CLIHelperError")


class CLIHelperError(Exception):
    """Base exception class for cli-helper-92 with rich metadata and code mapping."""

    default_exit_code: int = 1

    def __init__(
        self,
        message: str,
        *,
        exit_code: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.exit_code: int = exit_code if exit_code is not None else self.default_exit_code
        self.context: Dict[str, Any] = context or {}

    def format_cli_output(self, verbose: bool = False) -> str:
        """Format the exception message for command line output.

        Args:
            verbose: Include execution context dictionary if True.

        Returns:
            A human-readable formatted error string.
        """
        base: str = f"[Error {self.exit_code}] {self.message}"
        if verbose and self.context:
            details = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{base} | Context: {{{details}}}"
        return base

    @classmethod
    def raise_with_context(
        cls: Type[E], message: str, **kwargs: Any
    ) -> None:
        """Instantiate and raise an error with arbitrary context keyword args."""
        raise cls(message, context=kwargs)


class ConfigurationError(CLIHelperError):
    """Raised when application configuration is missing or invalid."""

    default_exit_code: int = 78


class CommandExecutionError(CLIHelperError):
    """Raised when a sub-command fails or exits with an unexpected code."""

    default_exit_code: int = 127


def handle_cli_exception(err: CLIHelperError, verbose: bool = False) -> None:
    """Standardized terminal error output routine and exit dispatcher.

    Args:
        err: The caught CLIHelperError instance.
        verbose: Output detailed contextual information if True.
    """
    sys.stderr.write(f"{err.format_cli_output(verbose=verbose)}\n")
    sys.exit(err.exit_code)
