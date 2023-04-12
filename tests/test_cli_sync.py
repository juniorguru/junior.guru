from juniorguru.cli.sync import get_parallel_chains, default_from_env


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


def test_get_parallel_chains_exclude():
    dependencies = {'a': [],
                    'b': ['a'],
                    'c': ['a'],
                    'd': [],
                    'e': ['d', 'c'],
                    'f': ['d']}

    assert get_parallel_chains(dependencies, exclude=['a']) == [['b'], ['c', 'd', 'e', 'f']]


def test_default_from_env(monkeypatch):
    monkeypatch.setenv('FOO', 'something')
    env_reader = default_from_env('FOO')

    assert env_reader() == 'something'


def test_default_from_env_default(monkeypatch):
    monkeypatch.delenv('FOO', raising=False)
    env_reader = default_from_env('FOO', default='something')

    assert env_reader() == 'something'


def test_default_from_env_type(monkeypatch):
    monkeypatch.setenv('FOO', '123')
    env_reader = default_from_env('FOO', type=int)

    assert env_reader() == 123


def test_default_from_env_type_default(monkeypatch):
    monkeypatch.delenv('FOO', raising=False)
    env_reader = default_from_env('FOO', default=123, type=int)

    assert env_reader() == 123
