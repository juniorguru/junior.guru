import pytest

from juniorguru.lib.global_state import load as load_global_state, save as save_global_state
from juniorguru.lib.mutations import MutationsNotAllowedError, allow, mutates, allow_all, is_allowed, forcing_allowed


@pytest.fixture
def global_state():
    dump = load_global_state()
    try:
        save_global_state(dict())
        yield
    finally:
        save_global_state(dump)


def test_basic_usage(global_state):
    allow('discord')

    @mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert isinstance(value_f, MutationsNotAllowedError)
    assert value_d == 2


@pytest.mark.asyncio
async def test_basic_usage_async(global_state):
    allow('discord')

    @mutates('fakturoid')
    async def fakturoid():
        return 1
    value_f = await fakturoid()

    @mutates('discord')
    async def discord():
        return 2
    value_d = await discord()

    assert isinstance(value_f, MutationsNotAllowedError)
    assert value_d == 2


def test_allow_multiple(global_state):
    allow('fakturoid', 'discord')

    @mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert value_f == 1
    assert value_d == 2


def test_allow_all(global_state):
    allow_all()

    @mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert value_f == 1
    assert value_d == 2


def test_is_allowed(global_state):
    allow('discord')

    assert is_allowed('fakturoid') is False
    assert is_allowed('discord') is True


def test_mutates_evaluates_during_call_time_not_import_time(global_state):
    @mutates('discord')
    def discord():
        return 123
    value1 = discord()

    allow('discord')
    value2 = discord()

    assert isinstance(value1, MutationsNotAllowedError)
    assert value2 == 123


def test_mutates_raises(global_state):
    @mutates('discord', raises=True)
    def discord():
        return 123

    with pytest.raises(MutationsNotAllowedError):
        discord()


def test_forcing_allowed(global_state):
    allow('fakturoid')

    assert is_allowed('discord') is False
    assert is_allowed('fakturoid') is True

    with forcing_allowed('discord'):
        assert is_allowed('discord') is True
        assert is_allowed('fakturoid') is False

    assert is_allowed('discord') is False
    assert is_allowed('fakturoid') is True
