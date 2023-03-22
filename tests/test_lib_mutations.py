import pytest

from juniorguru.lib.mutations import Mutations


def test_mutations_mutation():
    mutations = Mutations()
    mutations.allow('discord')

    def fakturoid():
        return 1
    fakturoid_fn = mutations.mutates('fakturoid')(fakturoid)
    fakturoid_val = fakturoid_fn()

    def discord():
        return 2
    discord_fn = mutations.mutates('discord')(discord)
    discord_val = discord_fn()

    assert fakturoid_val is mutations.MutationsNotAllowed
    assert discord_val == 2


@pytest.mark.asyncio
async def test_mutations_mutation_async():
    mutations = Mutations()
    mutations.allow('discord')

    async def fakturoid():
        return 1
    fakturoid_fn = mutations.mutates('fakturoid')(fakturoid)
    fakturoid_val = await fakturoid_fn()

    async def discord():
        return 2
    discord_fn = mutations.mutates('discord')(discord)
    discord_val = await discord_fn()

    assert fakturoid_val is mutations.MutationsNotAllowed
    assert discord_val == 2


def test_mutations_is_allowed():
    mutations = Mutations()
    mutations.allow('discord')

    assert mutations.is_allowed('fakturoid') is False
    assert mutations.is_allowed('discord') is True


def test_mutations_evaluate_during_call_time_not_import_time():
    mutations = Mutations()

    def discord():
        return 123
    fn = mutations.mutates('discord')(discord)
    val1 = fn()

    mutations.allow('discord')
    val2 = fn()

    assert val1 is mutations.MutationsNotAllowed
    assert val2 == 123
