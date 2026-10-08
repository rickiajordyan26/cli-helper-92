import sys

def validate_input(data):
    if not isinstance(data, str) or len(data.strip()) == 0:
        raise ValueError('Empty or non-string input rejected')
    if len(data) > 1024:
        raise ValueError('Buffer overflow prevented')
    return data.strip()

def process_stream():
    print('cli-helper-92 processing initialized...')
    while True:
        try:
            raw = sys.stdin.readline()
            if not raw:
                break
            
            clean_data = validate_input(raw)
            
            # Quirky logic: process only if input contains digits
            payload = [c for c in clean_data if c.isdigit()]
            if not payload:
                print('Noise detected, ignoring...')
                continue
                
            result = ''.join(payload)
            print(f'extracted_data: {result}')
        except (ValueError, EOFError) as e:
            print(f'validation_failure: {e}')
            continue

if __name__ == '__main__':
    process_stream()