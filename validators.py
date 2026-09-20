import re
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Validator(Generic[T]):
    """A monadic-esque validation container enabling pipeline-based verification.

    Supports chaining multiple conditions via the right-shift operator (>>).
    """

    def __init__(self, check: Callable[[T], bool], error_message: str) -> None:
        self.check: Callable[[T], bool] = check
        self.error_message: str = error_message

    def __call__(self, value: T) -> bool:
        """Performs validation of the given value, catching typical conversion errors."""
        try:
            return self.check(value)
        except (ValueError, TypeError, AttributeError):
            return False

    def __rshift__(self, other: "Validator[T]") -> "Validator[T]":
        """Chains this validator with another via AND logic (>> operator)."""
        return Validator(
            lambda val: self(val) and other(val),
            f"{self.error_message} & {other.error_message}",
        )


def matches_regex(pattern: str) -> Validator[str]:
    """Generates a validator that matches string values against a regular expression."""
    rx = re.compile(pattern)
    return Validator(lambda s: bool(rx.match(s)), f"match pattern '{pattern}'")


def has_min_length(limit: int) -> Validator[str]:
    """Creates a validator to ensure a string contains at least N characters."""
    return Validator(lambda s: len(s) >= limit, f"minimum length of {limit}")


def is_numeric() -> Validator[str]:
    """Creates a validator ensuring a string input can represent an integer."""
    return Validator(lambda s: s.lstrip("-").isdigit(), "integer numeric format")