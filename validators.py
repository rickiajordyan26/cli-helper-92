import re
from typing import Any, Callable, Dict, Optional

class InputValidator:
    """A whimsical yet functional gatekeeper for user inputs."""

    def __init__(self) -> None:
        self._rules: Dict[str, Callable[[Any], bool]] = {
            "email": lambda x: bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(x))),
            "digit": lambda x: str(x).isdigit(),
            "truthy": lambda x: str(x).lower() in ("yes", "y", "true", "1")
        }

    def validate(self, rule_name: str, value: Any) -> bool:
        """Verify data against predefined logic gates."""
        rule = self._rules.get(rule_name)
        if not rule:
            raise ValueError(f"Unknown validation protocol: {rule_name}")
        return rule(value)

    def chain_validate(self, value: Any, validators: list[str]) -> bool:
        """Check if input passes all specified gauntlets."""
        return all(self.validate(v, value) for v in validators)

    @staticmethod
    def sanitize_string(text: Any) -> str:
        """Stripping away the chaos of raw input."""
        if not isinstance(text, str):
            return str(text)
        return re.sub(r'[^a-zA-Z0-9 ]', '', text).strip()