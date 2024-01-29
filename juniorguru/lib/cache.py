from diskcache import Cache
import functools

from jinja2 import BytecodeCache as BaseBytecodeCache
from jinja2.bccache import Bucket

from juniorguru.lib import loggers


CACHE_DIR = ".cache"


logger = loggers.from_path(__file__)


@functools.cache()
def get_cache() -> Cache:
    logger.debug(f"Initializing cache: {CACHE_DIR}")
    return Cache(CACHE_DIR)


class BytecodeCache(BaseBytecodeCache):
    def __init__(self, cache: Cache):
        self.cache = cache

    def load_bytecode(self, bucket: Bucket):
        with self.cache.read(f"jinja:{bucket.key}") as f:
            bucket.load_bytecode(f)

    def dump_bytecode(self, bucket: Bucket):
        self.cache.set(f"jinja:{bucket.key}", bucket.bytecode_to_string(), tag="jinja")


@functools.cache()
def get_jinja_cache() -> BytecodeCache:
    return BytecodeCache(get_cache())
