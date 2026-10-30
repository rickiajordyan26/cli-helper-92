"""Validator engine providing composable validation rules for CLI inputs."""

from typing import Callable, Any, TypeVar, Generic, Sequence
import re

T = TypeVar("T")


class Rule(Generic[T]):
    """A composable validation rule wrapping a predicate function.
    
    Allows combining validation rules using bitwise operators (&, |, ~)
    to build expressively chained validation logic.
    """
    def __init__(self, predicate: Callable[[T], bool], message: str) -> None:
        self.predicate = predicate
        self.message = message

    def __call__(self, value: T) -> tuple[bool, str]:
        """Execute validation against the given value, returning pass status and error message."""
        is_valid = bool(self.predicate(value))
        return is_valid, "" if is_valid else self.message

    def __and__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules with logical AND."""
        return Rule(
            lambda val: self(val)[0] and other(val)[0],
            f"{self.message} AND {other.message}"
        )

    def __or__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules with logical OR."""
        return Rule(
            lambda val: self(val)[0] or other(val)[0],
            f"{self.message} OR {other.message}"
        )

    def __invert__(self) -> "Rule[T]":
        """Negate the validation rule logic."""
        return Rule(
            lambda val: not self(val)[0],
            f"NOT ({self.message})"
        )


def is_non_empty() -> Rule[str]:
    """Validates that string input is non-empty after stripping whitespace."""
    return Rule(lambda s: bool(s and s.strip()), "Value cannot be empty")


def is_numeric() -> Rule[str]:
    """Validates that string input represents a valid integer or float."""
    return Rule(
        lambda s: bool(re.match(r"^-?\d+(\.\d+)?$", s.strip())),
        "Value must be numeric"
    )


def matches_regex(pattern: str) -> Rule[str]:
    """Validates that string input matches a specific regular expression pattern."""
    compiled = re.compile(pattern)
    return Rule(lambda s: bool(compiled.search(s)), f"Value must match pattern: {pattern}")


def in_choices(choices: Sequence[Any]) -> Rule[Any]:
    """Validates that input exists within a defined sequence of choices."""
    return Rule(lambda val: val in choices, f"Value must be one of {list(choices)}")


def validate_all(value: Any, rules: Sequence[Rule[Any]]) -> list[str]:
    """Runs multiple validation rules against a single value, returning collected errors."""
    errors: list[str] = []
    for rule in rules:
        ok, msg = rule(value)
        if not ok:
            errors.append(msg)
    return errors
