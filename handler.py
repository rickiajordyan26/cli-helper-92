import json
from typing import Any, Dict, List, Union

class DataMorpher:
    """An unorthodox data transformation pipeline for cli-helper-92."""
    def __init__(self, depth: int = 3):
        self.depth = depth

    def process(self, data: Any, transform: callable) -> Any:
        """Recursively apply function with metadata injection."""
        if isinstance(data, dict):
            return {k: self.process(v, transform) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process(i, transform) for i in data]
        return transform(data)

def sanitize_input(value: Any) -> Any:
    """Flatten types and normalize cli inputs."""
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, (int, float)):
        return value * 1.0
    return str(value)

def stream_payload(payload: Union[Dict, List]) -> str:
    """Serialization of morphed data structures."""
    morpher = DataMorpher()
    refined = morpher.process(payload, sanitize_input)
    return json.dumps(refined, indent=2)

if __name__ == '__main__':
    sample = {'DEBUG': ' TRUE ', 'LEVEL': 10, 'TAGS': ['cli', '  Niche  ']}
    print(stream_payload(sample))