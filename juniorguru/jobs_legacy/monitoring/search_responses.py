import sys
from pathlib import Path
from subprocess import run


PROJECT_DIR = Path(__file__).parent.parent
RESPONSES_DIR = PROJECT_DIR / 'juniorguru' / 'data' / 'responses'


text = ' '.join(sys.argv[1:])
if not text.strip():
    print('Nothing to search for…', file=sys.stderr)
    sys.exit(1)

print('Searching for:', repr(text), file=sys.stderr)
run(['grep', text, '-l', '-r', RESPONSES_DIR], check=True, cwd=Path.cwd())
