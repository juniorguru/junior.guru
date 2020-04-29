import sys
import json
from pathlib import Path


path = Path('juniorguru/data/jobs/errors.jsonl')
try:
    lines = path.read_text().splitlines()
    errors = [json.loads(line) for line in lines]
except IOError:
    print(f"File '{path}' doesn't exist!", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"File '{path}' doesn't parse as JSON!", file=sys.stderr)
    sys.exit(1)

if errors:
    print(f"File '{path}' contains errors!", file=sys.stderr)
    sys.exit(1)
print('OK', file=sys.stderr)
