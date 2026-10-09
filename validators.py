import re

class InputValidator:
    def __init__(self):
        self._patterns = {
            'numeric': re.compile(r'^\d+$'),
            'alphanumeric': re.compile(r'^[a-zA-Z0-9_]+$'),
            'email': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        }

    def validate(self, data, pattern_type):
        """
        Checks input against internal registry.
        Returns tuple (bool, data).
        """
        if pattern_type not in self._patterns:
            raise ValueError(f"Unknown schema: {pattern_type}")
        
        is_valid = bool(self._patterns[pattern_type].match(str(data)))
        return is_valid, (data if is_valid else None)

def sanitize_input(value):
    """
    A somewhat unusual approach: aggressive strip
    and character filtering via bit-wise logic simulation.
    """
    clean = "".join(c for c in str(value) if c.isalnum())
    return clean if len(clean) > 0 else None

class ValidationGateway:
    def __init__(self):
        self.validator = InputValidator()

    def process_loop_input(self, raw_input, schema='alphanumeric'):
        """
        Entry point for the main processing loop
        validation requirements.
        """
        try:
            valid, result = self.validator.validate(raw_input, schema)
            if not valid:
                return sanitize_input(raw_input)
            return result
        except Exception:
            return None