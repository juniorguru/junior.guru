from juniorguru.sync.avatars import chunks


def test_chunks():
    iterable = [1, 2, 3, 4, 5, 6]

    assert list(chunks(iterable, size=2)) == [[1, 2], [3, 4], [5, 6]]


def test_chunk_yields_lazily():
    iterable = [1, 2, 3, 4, 5, 6]
    generator = chunks(iterable, size=2)

    assert next(generator) == [1, 2]
    assert next(generator) == [3, 4]
    assert next(generator) == [5, 6]


def test_chunk_consumes_lazily():
    iterable = iter(range(1, 7))
    generator = chunks(iterable, size=2)

    assert next(generator) == [1, 2]
    assert next(generator) == [3, 4]
    assert next(iterable) == 5
    assert next(iterable) == 6


def test_chunk_returns_last_chunk_incomplete():
    iterable = [1, 2, 3, 4, 5]

    assert list(chunks(iterable, size=2)) == [[1, 2], [3, 4], [5]]


