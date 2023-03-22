import pytest

from juniorguru.lib.mutations import (Mutations, MutationsNotAllowed,
                                      MutationsNotAllowedError,
                                      MutationsNotInitializedError)


def test_mutations_mutation():
    mutations = Mutations()
    mutations.allow('discord')

    @mutations.mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutations.mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert value_f is MutationsNotAllowed
    assert value_d == 2


@pytest.mark.asyncio
async def test_mutations_mutation_async():
    mutations = Mutations()
    mutations.allow('discord')

    @mutations.mutates('fakturoid')
    async def fakturoid():
        return 1
    value_f = await fakturoid()

    @mutations.mutates('discord')
    async def discord():
        return 2
    value_d = await discord()

    assert value_f is MutationsNotAllowed
    assert value_d == 2


def test_mutations_allow_multiple():
    mutations = Mutations()
    mutations.allow('fakturoid', 'discord')

    @mutations.mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutations.mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert value_f == 1
    assert value_d == 2


def test_mutations_allow_all():
    mutations = Mutations()
    mutations.allow_all()

    @mutations.mutates('fakturoid')
    def fakturoid():
        return 1
    value_f = fakturoid()

    @mutations.mutates('discord')
    def discord():
        return 2
    value_d = discord()

    assert value_f == 1
    assert value_d == 2


def test_mutations_is_allowed():
    mutations = Mutations()
    mutations.allow('discord')

    assert mutations.is_allowed('fakturoid') is False
    assert mutations.is_allowed('discord') is True


def test_mutations_evaluate_during_call_time_not_import_time():
    mutations = Mutations()
    mutations.allow()

    @mutations.mutates('discord')
    def discord():
        return 123
    value1 = discord()

    mutations.allow('discord')
    value2 = discord()

    assert value1 is MutationsNotAllowed
    assert value2 == 123


def test_mutations_raises():
    mutations = Mutations()
    mutations.allow()

    @mutations.mutates('discord', raises=True)
    def discord():
        return 123

    with pytest.raises(MutationsNotAllowedError):
        discord()


def test_mutations_must_be_initialized():
    mutations = Mutations()

    @mutations.mutates('discord')
    def discord():
        return 123

    with pytest.raises(MutationsNotInitializedError):
        mutations.is_allowed('fakturoid')
    with pytest.raises(MutationsNotInitializedError):
        discord()


def test_mutations_dump():
    mutations = Mutations()
    mutations.allow('discord', 'fakturoid')

    assert mutations.dump() == ['discord', 'fakturoid']


def test_mutations_load():
    mutations = Mutations()
    mutations.load(['discord', 'fakturoid'])

    assert mutations.is_allowed('discord')
    assert mutations.is_allowed('fakturoid')
