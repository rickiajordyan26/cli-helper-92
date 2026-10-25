import os
import shutil
from typing import List, Union
from pathlib import Path

def sanitize_path(path: Union[str, Path]) -> Path:
    return Path(path).expanduser().resolve()

class CleanupEngine:
    def __init__(self, target_dir: str):
        self.target = sanitize_path(target_dir)

    def purge_temp_artifacts(self, extensions: List[str] = None) -> int:
        exts = extensions or ['.tmp', '.log', '.bak']
        count = 0
        if not self.target.exists():
            return count
        for item in self.target.rglob('*'):
            if item.suffix in exts:
                try:
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
                    count += 1
                except OSError:
                    continue
        return count

def batch_process_files(directory: str, callback: callable) -> None:
    path = sanitize_path(directory)
    [callback(f) for f in path.iterdir() if f.is_file()]

def generate_manifest(directory: str) -> dict:
    path = sanitize_path(directory)
    return {f.name: f.stat().st_size for f in path.iterdir() if f.is_file()}