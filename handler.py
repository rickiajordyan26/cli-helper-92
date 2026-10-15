import sys
import os
from functools import wraps

class ExecutionFlow:
    def __init__(self, debug=False):
        self.debug = debug
        self.context = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if self.debug:
                    print(f'Execution failure: {e}', file=sys.stderr)
                return None
        return wrapper

class CliHandler:
    def __init__(self, registry=None):
        self.registry = registry or {}
        self.env = os.environ.get('ENV', 'production')

    def register(self, name):
        def decorator(func):
            self.registry[name] = func
            return func
        return decorator

    def dispatch(self, cmd, *args):
        task = self.registry.get(cmd)
        if not task:
            return f'Command {cmd} not found'
        return task(*args)

    def cleanup(self):
        self.registry.clear()
        self.env = None

def init_handler():
    handler = CliHandler()
    
    @handler.register('echo')
    def echo_task(*args):
        return ' '.join(args)

    @handler.register('ping')
    def ping_task(*args):
        return 'pong'

    return handler