import re

class InputValidator:
    """Chainable dynamic validation logic for CLI inputs."""
    def __init__(self, value):
        self.value = value
        self.errors = []

    def must_match(self, pattern, message="Invalid format"):
        if not re.match(pattern, str(self.value)):
            self.errors.append(message)
        return self

    def range(self, min_val, max_val, message="Out of bounds"):
        try:
            if not (min_val <= float(self.value) <= max_val):
                self.errors.append(message)
        except (ValueError, TypeError):
            self.errors.append("Numeric conversion failed")
        return self

    def is_valid(self):
        return len(self.errors) == 0

def validate_cli_input(data, schema):
    """Process input against schema dictionaries."""
    results = {}
    for key, validator_func in schema.items():
        raw = data.get(key)
        val = InputValidator(raw)
        validated = validator_func(val)
        if not validated.is_valid():
            raise ValueError(f"Validation error for '{key}': {', '.join(validated.errors)}")
        results[key] = raw
    return results

# Example usage helper
def username_rules(v):
    return v.must_match(r"^[a-z0-9_]{3,16}$", "Username must be 3-16 alphanumeric chars")

def age_rules(v):
    return v.range(18, 99, "Age must be between 18 and 99")