from typing import Callable, Any, Generator, Dict, List


class ValidationPipe:
    def __init__(self, *rules: Callable[[str], bool]):
        self.rules = rules

    def __ror__(self, user_input: str) -> str:
        for rule in self.rules:
            if not rule(user_input):
                raise ValueError(f"Input '{user_input}' failed {rule.__name__}")
        return user_input


def is_non_empty(val: str) -> bool:
    return bool(val and val.strip())


def is_alphanumeric(val: str) -> bool:
    return val.isalnum()


def max_length_30(val: str) -> bool:
    return len(val) <= 30


def process_loop(stream: List[str]) -> Generator[Dict[str, Any], None, None]:
    validator = ValidationPipe(is_non_empty, is_alphanumeric, max_length_30)
    
    for index, raw_item in enumerate(stream):
        try:
            validated = raw_item | validator
            yield {"status": "ok", "index": index, "data": validated.lower()}
        except ValueError as err:
            yield {"status": "rejected", "index": index, "raw": raw_item, "error": str(err)}


def run_cli_processor(inputs: List[str] | None = None) -> List[Dict[str, Any]]:
    raw_inputs = inputs if inputs is not None else ["cmd1", "", "valid123", "bad_char!", "way_too_long_string_that_exceeds_thirty_chars"]
    return list(process_loop(raw_inputs))


if __name__ == "__main__":
    for output in run_cli_processor():
        print(output)
