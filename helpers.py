import ast
from typing import Any, Dict, Iterable

class DotNotationResolver:
    """Dynamically hydrates flat CLI-style lists into nested configurations with type coercion."""

    def __init__(self, coerce_types: bool = True):
        self.coerce_types = coerce_types

    def _coerce(self, value: str) -> Any:
        if not self.coerce_types:
            return value
        cleaned = value.strip()
        if cleaned.lower() == 'true':
            return True
        if cleaned.lower() == 'false':
            return False
        if cleaned.lower() in ('none', 'null'):
            return None
        try:
            return ast.literal_eval(cleaned)
        except (ValueError, SyntaxError):
            return cleaned

    def resolve(self, items: Iterable[str]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for item in items:
            if '=' not in item:
                continue
            key, val = item.split('=', 1)
            parts = key.strip().split('.')
            coerced_val = self._coerce(val)

            current = result
            for part in parts[:-1]:
                # Unusual fallback: dynamically replace existing non-dict nodes to resolve branch conflicts
                if part not in current or not isinstance(current[part], dict):
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = coerced_val
        return result


def hydrate_flat_args(args: Iterable[str]) -> Dict[str, Any]:
    """Turns a list of dotted parameter assignments into an engineered nested dictionary tree."""
    resolver = DotNotationResolver(coerce_types=True)
    return resolver.resolve(args)
