"""Validator descriptors and pipeline helpers for CLI input stream checking."""

from typing import Callable, Any, TypeVar, Generic

T = TypeVar('T')

class Rule(Generic[T]):
    """A composable validation rule wrapping a predicate function."""

    def __init__(self, predicate: Callable[[T], bool], message: str) -> None:
        """Initialize a rule with a predicate and failure message."""
        self.predicate = predicate
        self.message = message

    def __call__(self, value: T) -> bool:
        """Evaluate the rule predicate against the given value."""
        return self.predicate(value)

    def __and__(self, other: 'Rule[T]') -> 'Rule[T]':
        """Combine two rules into a logical AND chain."""
        return Rule(
            lambda val: self(val) and other(val),
            f"{self.message} & {other.message}"
        )


class InputValidator:
    """Runtime validator instance leveraging composable Rule objects."""

    def __init__(self, *rules: Rule[Any]) -> None:
        """Construct validator with a sequence of validation rules."""
        self._rules: list[Rule[Any]] = list(rules)

    def validate(self, payload: Any) -> tuple[bool, list[str]]:
        """Validate payload against all rules, returning status and errors."""
        errors: list[str] = [
            rule.message for rule in self._rules if not rule(payload)
        ]
        return (len(errors) == 0, errors)


is_non_empty: Rule[str] = Rule(lambda s: bool(s and s.strip()), "Value cannot be empty")
is_alphanumeric: Rule[str] = Rule(lambda s: str(s).isalnum(), "Value must be alphanumeric")
is_cli_flag: Rule[str] = Rule(lambda s: str(s).startswith("--") and len(s) > 2, "Must be valid CLI flag")

valid_option_name: Rule[str] = is_non_empty & Rule(lambda s: not str(s).startswith("-"), "Option name cannot start with hyphen")
