from types import SimpleNamespace

import pytest
from diskcache import Cache

from jg.coop.lib import cache as cache_module
from jg.coop.lib.cache import cache


@pytest.fixture
def disk_cache(tmp_path, monkeypatch):
    disk_cache = Cache(tmp_path)
    monkeypatch.setattr(
        cache_module, "_cache_instances", {cache_module.CACHE_DIR: disk_cache}
    )
    yield disk_cache
    disk_cache.close()


def make_failing_fn(**cache_kwargs):
    calls = SimpleNamespace(count=0)

    @cache(**cache_kwargs)
    async def fn(value: str) -> str:
        calls.count += 1
        raise ValueError(f"Unable to process: {value!r}")

    return fn, calls


@pytest.mark.asyncio
async def test_cache_errors_reraises(disk_cache):
    fn, _ = make_failing_fn(errors=(ValueError,))
    with pytest.raises(ValueError):
        await fn("foo")

    with pytest.raises(ValueError, match="Unable to process: 'foo'"):
        await fn("foo")


@pytest.mark.asyncio
async def test_cache_errors_calls_once(disk_cache):
    fn, calls = make_failing_fn(errors=(ValueError,))
    for _ in range(3):
        with pytest.raises(ValueError):
            await fn("foo")

    assert calls.count == 1


@pytest.mark.asyncio
async def test_cache_errors_not_configured(disk_cache):
    fn, calls = make_failing_fn()
    for _ in range(3):
        with pytest.raises(ValueError):
            await fn("foo")

    assert calls.count == 3


@pytest.mark.asyncio
async def test_cache_errors_other_error_not_cached(disk_cache):
    fn, calls = make_failing_fn(errors=(KeyError,))
    for _ in range(3):
        with pytest.raises(ValueError):
            await fn("foo")

    assert calls.count == 3


@pytest.mark.asyncio
async def test_cache_errors_tagged(disk_cache):
    fn, _ = make_failing_fn(errors=(ValueError,), tag="test-tag")
    with pytest.raises(ValueError):
        await fn("foo")

    assert disk_cache.evict("test-tag") == 1


@pytest.mark.asyncio
async def test_cache_results(disk_cache):
    calls = SimpleNamespace(count=0)

    @cache(errors=(ValueError,))
    async def fn(value: str) -> str:
        calls.count += 1
        return value.upper()

    results = [await fn("foo") for _ in range(3)]

    assert (results, calls.count) == (["FOO"] * 3, 1)


def test_cache_errors_sync_not_supported(disk_cache):
    with pytest.raises(NotImplementedError):

        @cache(errors=(ValueError,))
        def fn(value: str) -> str:
            return value
