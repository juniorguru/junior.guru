import asyncio

import pytest
from diskcache import Cache

import jg.coop.lib.mutations as mutations_module
from jg.coop.lib.mutations import (
    MutationsNotAllowedError,
    _set_allowed,
    allow,
    allow_none,
    is_allowed,
    mutates,
    mutating,
)


@pytest.fixture
def nothing_allowed(monkeypatch, tmp_path):
    cache = Cache(str(tmp_path / "mutations-cache"))
    monkeypatch.setattr(mutations_module, "get_cache", lambda: cache)

    _set_allowed([])
    try:
        yield
    finally:
        _set_allowed([])
        cache.close()


class Something:
    def __init__(self, property):
        self.property = property

    def method(self, a, b):
        return a + b

    async def async_method(self, a, b):
        await asyncio.sleep(0)
        return a + b


def test_basic_usage(nothing_allowed):
    allow("discord")

    @mutates("fakturoid")
    def fakturoid():
        return 1

    value_f = fakturoid()

    @mutates("discord")
    def discord():
        return 2

    value_d = discord()

    assert isinstance(value_f, MutationsNotAllowedError)
    assert value_d == 2


@pytest.mark.asyncio
async def test_basic_usage_async(nothing_allowed):
    allow("discord")

    @mutates("fakturoid")
    async def fakturoid():
        return 1

    value_f = await fakturoid()

    @mutates("discord")
    async def discord():
        return 2

    value_d = await discord()

    assert isinstance(value_f, MutationsNotAllowedError)
    assert value_d == 2


def test_allow_multiple(nothing_allowed):
    allow("fakturoid", "discord")

    @mutates("fakturoid")
    def fakturoid():
        return 1

    value_f = fakturoid()

    @mutates("discord")
    def discord():
        return 2

    value_d = discord()

    assert value_f == 1
    assert value_d == 2


def test_allow_none(nothing_allowed):
    allow("fakturoid", "discord")

    @mutates("fakturoid")
    def fakturoid():
        return 1

    @mutates("discord")
    def discord():
        return 2

    value_f = fakturoid()
    value_d = discord()

    assert value_f == 1
    assert value_d == 2

    allow_none()

    value_f = fakturoid()
    value_d = discord()

    assert isinstance(value_f, MutationsNotAllowedError)
    assert isinstance(value_d, MutationsNotAllowedError)


def test_is_allowed(nothing_allowed):
    allow("discord")

    assert is_allowed("fakturoid") is False
    assert is_allowed("discord") is True


def test_mutates_evaluates_during_call_time_not_import_time(nothing_allowed):
    @mutates("discord")
    def discord():
        return 123

    value1 = discord()

    allow("discord")
    value2 = discord()

    assert isinstance(value1, MutationsNotAllowedError)
    assert value2 == 123


def test_mutates_raises(nothing_allowed):
    @mutates("discord", raises=True)
    def func():
        return 123

    with pytest.raises(MutationsNotAllowedError):
        func()


def test_mutating_proxy_allowed(nothing_allowed):
    allow("discord")
    obj = Something(123)

    with mutating("discord", obj) as proxy:
        result1 = proxy.property
        result2 = proxy.method(4, 4)

    assert result1 == 123
    assert result2 == 8


def test_mutating_proxy_not_allowed(nothing_allowed):
    obj = Something(123)

    with mutating("discord", obj) as proxy:
        result1 = proxy.property
        result2 = proxy.method(4, 4)

    assert result1 == 123
    assert isinstance(result2, MutationsNotAllowedError)


def test_mutating_proxy_not_allowed_raises(nothing_allowed):
    obj = Something(123)

    with pytest.raises(MutationsNotAllowedError):
        with mutating("discord", obj, raises=True) as proxy:
            proxy.method(4, 4)


@pytest.mark.asyncio
async def test_mutating_proxy_allowed_async(nothing_allowed):
    allow("discord")
    obj = Something(123)

    with mutating("discord", obj) as proxy:
        result = await proxy.async_method(4, 4)

    assert result == 8


@pytest.mark.asyncio
async def test_mutating_proxy_not_allowed_async(nothing_allowed):
    obj = Something(123)

    with mutating("discord", obj) as proxy:
        result = await proxy.async_method(4, 4)

    assert isinstance(result, MutationsNotAllowedError)


@pytest.mark.asyncio
async def test_mutating_proxy_not_allowed_async_raises(nothing_allowed):
    obj = Something(123)

    with pytest.raises(MutationsNotAllowedError):
        with mutating("discord", obj, raises=True) as proxy:
            await proxy.async_method(4, 4)


def test_mutations_not_allowed_works_as_boolean(nothing_allowed):
    obj = Something(123)

    with mutating("discord", obj) as proxy:
        result = proxy.method(4, 4)

    assert isinstance(result, MutationsNotAllowedError)
    assert not result


def test_allow_blocks_reconfiguration(nothing_allowed):
    allow("discord")

    assert is_allowed("discord") is True

    with pytest.raises(RuntimeError, match="already configured"):
        allow("fakturoid")

    allow_none()

    assert is_allowed("discord") is False


def test_allow_none_is_permissive_while_configured(nothing_allowed):
    allow("discord")
    allow_none()

    assert is_allowed("discord") is False


def test_allow_none_is_idempotent(nothing_allowed):
    allow("discord")
    allow_none()
    allow_none()

    assert is_allowed("discord") is False
