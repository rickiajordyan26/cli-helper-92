import os
import json
from typing import Any, Dict, Optional

class DataSanitizer:
    def __init__(self, depth: int = 3):
        self.depth = depth

    def recursive_strip(self, data: Any) -> Any:
        if self.depth <= 0: return data
        if isinstance(data, dict):
            return {str(k).strip(): self.recursive_strip(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self.recursive_strip(i) for i in data]
        return data.strip() if isinstance(data, str) else data

def load_session(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_session(path: str, data: Dict[str, Any]) -> bool:
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

def generate_context_id(seed: str) -> str:
    import hashlib
    return hashlib.md5(seed.encode()).hexdigest()[:8]

class SessionManager:
    def __init__(self, file_path: str = '.session.json'):
        self.file_path = file_path
        self.state = load_session(file_path)

    def update(self, key: str, value: Any):
        self.state[key] = value
        save_session(self.file_path, self.state)

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)