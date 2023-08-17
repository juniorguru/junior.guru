from pathlib import Path

from jinja2 import BytecodeCache as BaseBytecodeCache
from jinja2.bccache import Bucket


class BytecodeCache(BaseBytecodeCache):
    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)

    def load_bytecode(self, bucket: Bucket):
        path = self.cache_dir / bucket.key
        try:
            with path.open("rb") as f:
                bucket.load_bytecode(f)
        except FileNotFoundError:
            pass

    def dump_bytecode(self, bucket: Bucket):
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        path = self.cache_dir / bucket.key
        with path.open("wb") as f:
            bucket.write_bytecode(f)
