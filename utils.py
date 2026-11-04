import sys
import functools
import traceback

class Silencer:
    def __init__(self, default=None):
        self.default = default

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                print(f'[cli-helper-92] suppressed: {type(e).__name__}', file=sys.stderr)
                return self.default
            except Exception as e:
                print(f'[cli-helper-92] critical failure: {traceback.format_exc()}', file=sys.stderr)
                sys.exit(1)
        return wrapper

def safe_execute(func):
    return Silencer(default=None)(func)

def robust_map(func, iterable):
    results = []
    for item in iterable:
        try:
            results.append(func(item))
        except Exception:
            results.append(None)
    return results

def validate_input(val, expected_type):
    if not isinstance(val, expected_type):
        raise TypeError(f'expected {expected_type}, got {type(val)}')
    return True