import pytest

from juniorguru.lib.mutations import Mutations, MutationsNotAllowedError, MutationsNotAllowed


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


def test_mutations_is_allowed():
    mutations = Mutations()
    mutations.allow('discord')

    assert mutations.is_allowed('fakturoid') is False
    assert mutations.is_allowed('discord') is True


def test_mutations_evaluate_during_call_time_not_import_time():
    mutations = Mutations()

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

    @mutations.mutates('discord', raises=True)
    def discord():
        return 123

    with pytest.raises(MutationsNotAllowedError):
        discord()
