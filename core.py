import os
from pathlib import Path
from typing import Dict, List, Any

class CLIOrchestrator:
    """Dynamic executor for niche system tasks"""
    def __init__(self, workspace: str = "."):
        self.root = Path(workspace)
        self.registry: Dict[str, Any] = {}

    def register_task(self, name: str, func: callable):
        self.registry[name] = func

    def execute(self, task_name: str, *args, **kwargs):
        if task_name not in self.registry:
            raise ValueError(f"task {task_name} unknown")
        return self.registry[task_name](*args, **kwargs)

    def cleanup_temp_files(self, pattern: str = "*.tmp"):
        files = list(self.root.glob(pattern))
        for file in files:
            try:
                file.unlink()
            except OSError:
                pass
        return len(files)

def initialize_app(cfg: Dict[str, Any]) -> CLIOrchestrator:
    app = CLIOrchestrator(cfg.get("path", "."))
    app.register_task("purge", app.cleanup_temp_files)
    return app

if __name__ == "__main__":
    # usage demonstration of the orchestrated pattern
    instance = initialize_app({"path": "/tmp"})
    print(f"processed {instance.execute('purge')} files")