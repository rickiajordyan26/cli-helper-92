import re

class InputGuardian:
    def __init__(self, patterns=None):
        self.patterns = patterns or {
            'int': r'^\d+$',
            'alpha': r'^[a-zA-Z]+$',
            'slug': r'^[a-z0-9-]+$'
        }

    def validate(self, value, rule):
        if rule not in self.patterns:
            raise ValueError(f"Unknown schema: {rule}")
        return bool(re.match(self.patterns[rule], str(value)))

def sanitize_input(user_input):
    """ strips dangerous chars and ensures clean string processing """
    return re.sub(r'[^\w\s-]', '', user_input.strip())

def enforce_schema(data, schema_map):
    guardian = InputGuardian()
    results = {}
    errors = []
    for key, rule in schema_map.items():
        val = data.get(key)
        if val and guardian.validate(val, rule):
            results[key] = val
        else:
            errors.append(f"field {key} failed validation for {rule}")
    
    if errors:
        return None, errors
    return results, None

# Example usage wrapper for main loops
def validate_loop_input(raw_input, schema):
    clean_data = {k: sanitize_input(v) for k, v in raw_input.items()}
    return enforce_schema(clean_data, schema)