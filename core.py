import sys
from typing import Callable, Any, Dict

class WorkflowManager:
    def __init__(self):
        self._tasks: Dict[str, Callable] = {}

    def register(self, name: str):
        def decorator(func: Callable):
            self._tasks[name] = func
            return func
        return decorator

    def execute(self, name: str, *args, **kwargs) -> Any:
        return self._tasks.get(name, lambda *a, **k: None)(*args, **kwargs)

    def cleanup(self):
        self._tasks.clear()
        print("registry state reset")

def run_pipeline(func: Callable):
    try:
        return func()
    except Exception as e:
        print(f"execution fault: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    manager = WorkflowManager()

    @manager.register("ping")
    def ping_service():
        return "pong"

    result = run_pipeline(lambda: manager.execute("ping"))
    print(result)
    manager.cleanup()