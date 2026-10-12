from typing import Any, Optional, Dict

class DataProcessingError(Exception):
    """Base exception for data operations in cli-helper-92."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}

class DataTransformationError(DataProcessingError):
    """Raised when raw data fails to map to required schema."""
    pass

class SchemaValidationWarning(Warning):
    """Non-fatal mismatch encountered during data normalization."""
    pass

def raise_if_empty(data: Any, key: str) -> None:
    """Sentinel check for required payload keys."""
    if not data or key not in data or data[key] is None:
        raise DataProcessingError(
            f"Missing critical key: {key}",
            context={"provided_data": str(data)[:50]}
        )

def safe_extract(data: Dict, key: str, default: Any = None) -> Any:
    """Duck-typed getter with structural logging context."""
    try:
        return data.get(key, default)
    except AttributeError:
        raise DataTransformationError(
            "Malformed container passed to extractor",
            context={"type": type(data).__name__}
        )