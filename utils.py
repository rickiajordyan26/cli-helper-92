import sys
import functools
from typing import Callable, Any, Dict, Optional

class ExecutionDegraded(UserWarning):
    """Warning emitted when an operation falls back to a safe stub."""
    pass

def resilient_execution(
    fallback_value: Any = None,
    suppress: tuple = (Exception,),
    telemetry_store: Optional[Dict[str, int]] = None
) -> Callable:
    """Decorator intercepting edge-case exceptions with dynamic safe fallbacks."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except suppress as err:
                if telemetry_store is not None:
                    err_key = err.__class__.__name__
                    telemetry_store[err_key] = telemetry_store.get(err_key, 0) + 1
                
                if isinstance(err, (BrokenPipeError, KeyboardInterrupt)):
                    try:
                        sys.stderr.close()
                    except Exception:
                        pass
                    sys.exit(130 if isinstance(err, KeyboardInterrupt) else 0)
                
                if isinstance(err, UnicodeDecodeError):
                    raw = getattr(err, 'object', b'')
                    if isinstance(raw, bytes):
                        return raw.decode('utf-8', errors='replace')

                if callable(fallback_value):
                    return fallback_value(err, *args, **kwargs)
                return fallback_value
        return wrapper
    return decorator

def safe_cli_stream(stream_func: Callable) -> Callable:
    """Wraps CLI generators to swallow stream crashes cleanly."""
    @functools.wraps(stream_func)
    def generator_wrapper(*args: Any, **kwargs: Any):
        try:
            yield from stream_func(*args, **kwargs)
        except (EOFError, StopIteration, MemoryError) as exc:
            sys.stderr.write(f"\n[cli-helper] Stream interrupted: {exc}\n")
            return
    return generator_wrapper