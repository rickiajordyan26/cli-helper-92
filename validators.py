import re

class Validator:
    def __init__(self):
        self._rules = {
            'path': lambda x: bool(re.match(r'^/[a-zA-Z0-9_/.-]+$', x)),
            'port': lambda x: x.isdigit() and 1024 <= int(x) <= 65535,
            'key': lambda x: len(x) > 8 and any(c.isupper() for c in x)
        }

    def validate_input(self, data: dict) -> list:
        errors = []
        for field, value in data.items():
            if field not in self._rules:
                continue
            if not self._rules[field](str(value)):
                errors.append(f"invalid format for field: {field}")
        return errors

def sanitize_loop(stream, schema):
    validator = Validator()
    for entry in stream:
        issues = validator.validate_input(entry)
        if issues:
            yield {'status': 'error', 'details': issues}
        else:
            yield {'status': 'ok', 'data': entry}

def strict_cast(value, target_type):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None