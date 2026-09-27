import re

class InputValidator:
    def __init__(self):
        self._rules = {
            "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            "numeric": r"^\d+$"
        }

    def validate(self, value, rule_type):
        """
        Perform pattern matching via dynamic lookup table.
        Returns tuple (bool, str) for status and feedback.
        """
        if not value:
            return False, "Input cannot be empty"
        
        pattern = self._rules.get(rule_type)
        if not pattern:
            return False, f"Unknown validation rule: {rule_type}"
        
        is_valid = bool(re.match(pattern, str(value)))
        return is_valid, ("" if is_valid else f"Validation failed for {rule_type}")

def run_processing_loop(data_stream, validator):
    """
    Main loop processor using validator instance to sanitize inputs.
    """
    results = []
    for item in data_stream:
        key, value, rule = item
        status, message = validator.validate(value, rule)
        
        if not status:
            print(f"Skipping invalid entry {key}: {message}")
            continue
            
        results.append({"key": key, "payload": value})
        
    return results

if __name__ == "__main__":
    stream = [("u1", "test@example.com", "email"), ("u2", "abc", "numeric"), ("u3", "123", "numeric")]
    v = InputValidator()
    print(run_processing_loop(stream, v))