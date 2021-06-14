import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from juniorguru.lib.magic import do_magic

do_magic()
