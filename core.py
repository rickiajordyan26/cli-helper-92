import sys
import inspect
from typing import Callable, Any, Dict, List, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

class QuickCLI:
    """A self-documenting CLI dispatcher utilizing runtime type coercion."""

    def __init__(self, description: str = "Unorthodox dynamic CLI runner") -> None:
        self.description: str = description
        self._commands: Dict[str, Callable[..., Any]] = {}

    def register(self, func: F) -> F:
        """Decorator to register a function as an executable CLI command."""
        self._commands[func.__name__] = func
        return func

    def _coerce(self, value: str, expected_type: Any) -> Any:
        """Coerce raw string inputs into designated annotation types."""
        if expected_type is bool:
            return value.lower() in ("true", "1", "yes")
        try:
            return expected_type(value)
        except (TypeError, ValueError):
            return value

    def run(self, args: List[str]) -> None:
        """Parse command-line arguments and route to the correct registered task."""
        if not args or args[0] in ("-h", "--help"):
            print(f"{self.description}\n\nAvailable commands:")
            for name, cmd in self._commands.items():
                print(f"  {name:15} {cmd.__doc__ or 'No description.'}")
            return

        cmd_name = args[0]
        if cmd_name not in self._commands:
            print(f"Unknown command: {cmd_name}", file=sys.stderr)
            sys.exit(1)

        func = self._commands[cmd_name]
        sig = inspect.signature(func)
        raw_args = args[1:]
        
        pos_params = [p for p in sig.parameters.values() if p.default == inspect.Parameter.empty]
        if len(raw_args) < len(pos_params):
            print(f"Error: {cmd_name} expects {len(pos_params)} arguments.", file=sys.stderr)
            sys.exit(1)

        coerced: List[Any] = []
        for i, param in enumerate(sig.parameters.values()):
            if i < len(raw_args):
                coerced.append(self._coerce(raw_args[i], param.annotation))
            elif param.default != inspect.Parameter.empty:
                coerced.append(param.default)

        result = func(*coerced)
        if result is not None:
            print(result)