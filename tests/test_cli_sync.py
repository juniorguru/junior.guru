from juniorguru.cli.sync import get_parallel_chains


def test_get_parallel_chains():
    dependencies = {'a': [],
                    'b': ['a'],
                    'c': []}

    assert get_parallel_chains(dependencies) == [['a', 'b'], ['c']]


def test_get_parallel_chains_sorted():
    dependencies = {'c': [],
                    'f': [],
                    'b': ['f'],
                    'a': [],}

    assert get_parallel_chains(dependencies) == [['a'], ['b', 'f'], ['c']]


def test_get_parallel_chains_multiple_require_same_command():
    dependencies = {'a': [],
                    'b': ['a'],
                    'c': ['a'],
                    'd': []}

    assert get_parallel_chains(dependencies) == [['a', 'b', 'c'], ['d']]


def test_get_parallel_chains_interconnected_chains():
    dependencies = {'a': [],
                    'b': ['a'],
                    'c': ['a'],
                    'd': [],
                    'e': ['d', 'c'],
                    'f': ['d']}

    assert get_parallel_chains(dependencies) == [['a', 'b', 'c', 'd', 'e', 'f']]
