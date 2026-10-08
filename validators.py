import sys
import unicodedata
from typing import Any, Callable, List

class ValidationError(ValueError):
    """Custom exception for CLI argument irregularities."""
    pass

class EdgeCaseValidator:
    """CLI input validator targeting complex structural edge cases."""

    def __init__(self) -> None:
        self._validators: List[Callable[[str], None]] = [
            self._check_invisible_unicode,
            self._check_shell_poisoning,
            self._check_repetitive_bloat,
        ]

    def _check_invisible_unicode(self, data: str) -> None:
        for char in data:
            cat = unicodedata.category(char)
            if cat in ("Cf", "Zl", "Zp") or (cat == "Zs" and char != " "):
                raise ValidationError(
                    f"Invisible or unsafe unicode sequence detected: U+{ord(char):04X} ({cat})"
                )

    def _check_shell_poisoning(self, data: str) -> None:
        for sequence in [";", "&&", "||", "$(", "`", "\x00", "\n", "\r"]:
            if sequence in data:
                raise ValidationError(
                    f"Potential shell injection sequence containing '{sequence}' detected"
                )

    def _check_repetitive_bloat(self, data: str) -> None:
        if len(data) > 1024:
            raise ValidationError("Input size limits exceeded for standard CLI buffer safety")
        if any(data.count(char) > 256 for char in set(data)):
            raise ValidationError("Adversarial repeating-character input pattern detected")

    def validate(self, input_value: Any) -> str:
        """Main validation entrypoint with strict character verification."""
        if input_value is None:
            raise ValidationError("Input cannot be void/None")
        
        try:
            processed = str(input_value).encode("utf-8", errors="strict").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError) as err:
            raise ValidationError(f"Strict encoding verification failed: {err}")

        for checker in self._validators:
            checker(processed)

        return processed
