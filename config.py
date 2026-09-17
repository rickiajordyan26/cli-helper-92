"""Dynamic configuration cascade engine for CLI options."""

import os
from typing import Any, TypeVar, Callable, Generic, Dict, Optional, Union

T = TypeVar("T")


class ConfigValue(Generic[T]):
    """Descriptor resolving dynamic configuration values with type casting."""

    def __init__(self, key: str, default: T, cast: Optional[Callable[[Any], T]] = None) -> None:
        """Initialize a typed configuration key descriptor."""
        self.key = key
        self.default = default
        self.cast = cast or (lambda x: type(default)(x))

    def __get__(self, instance: Any, owner: Any) -> T:
        """Retrieve and cast value from environment or internal cache."""
        if instance is None:
            return self.default
        raw_val = instance._data.get(self.key, os.getenv(self.key.upper(), self.default))
        try:
            return self.cast(raw_val) if raw_val != self.default else self.default
        except (ValueError, TypeError):
            return self.default


class DynamicConfig:
    """Config registry utilizing bitwise OR syntax for merging instances."""

    verbose: ConfigValue[bool] = ConfigValue("verbose", False, lambda x: str(x).lower() in ("true", "1", "yes"))
    max_retries: ConfigValue[int] = ConfigValue("max_retries", 3, int)
    output_format: ConfigValue[str] = ConfigValue("output_format", "json", str)

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None) -> None:
        """Initialize config instance with dictionary payload."""
        self._data: Dict[str, Any] = initial_data or {}

    def __or__(self, other: Union["DynamicConfig", Dict[str, Any]]) -> "DynamicConfig":
        """Merge two config instances or a dict using the bitwise OR operator."""
        merged = self._data.copy()
        if isinstance(other, DynamicConfig):
            merged.update(other._data)
        elif isinstance(other, dict):
            merged.update(other)
        return DynamicConfig(merged)

    def to_dict(self) -> Dict[str, Any]:
        """Export active config options into dictionary form."""
        return {
            "verbose": self.verbose,
            "max_retries": self.max_retries,
            "output_format": self.output_format,
        }
