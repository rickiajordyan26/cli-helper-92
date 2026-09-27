import sys
import functools
import traceback

def robust_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            ctx = {
                'func': func.__name__,
                'args': args,
                'error': str(e),
                'trace': traceback.format_exc()
            }
            _dump_to_emergency_buffer(ctx)
            return None
    return wrapper

def _dump_to_emergency_buffer(data):
    try:
        with open('.emergency_log', 'a') as f:
            f.write(f"{repr(data)}\n")
    except Exception:
        sys.stderr.write("Emergency logging failure: critical system state.\n")

@robust_log
def safe_execute(action, *args):
    if not callable(action):
        raise ValueError(f"Action {action} is not executable")
    return action(*args)