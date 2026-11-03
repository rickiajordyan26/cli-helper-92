import os
import shutil
from pathlib import Path
from typing import List, Callable

class CleanupEngine:
    def __init__(self, target_dir: str):
        self.target_path = Path(target_dir)

    def run_sanitization(self, filters: List[Callable[[Path], bool]]) -> None:
        if not self.target_path.exists():
            return
        for item in self.target_path.iterdir():
            if all(f(item) for f in filters):
                self._obliterate(item)

    def _obliterate(self, path: Path) -> None:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

def is_temp_file(p: Path) -> bool:
    return p.suffix in {'.tmp', '.log', '.bak'}

def is_stale_dir(p: Path) -> bool:
    return p.is_dir() and p.name.startswith('__')

if __name__ == '__main__':
    engine = CleanupEngine(os.getcwd())
    engine.run_sanitization([is_temp_file])
    engine.run_sanitization([is_stale_dir])