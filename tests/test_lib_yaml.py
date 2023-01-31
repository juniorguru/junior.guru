from datetime import date

import pytest
from strictyaml import Map, load

from juniorguru.lib.yaml import Date


def test_date():
    assert load('starts_on: 2023-01-30', Map({'starts_on': Date()})).data == {'starts_on': date(2023, 1, 30)}


def test_date_raises_on_nonsense_value():
    with pytest.raises(ValueError):
        assert load('starts_on: 123', Map({'starts_on': Date()}))


def test_date_raises_on_datetime_value():
    with pytest.raises(ValueError):
        assert load('starts_on: 2016-10-22T14:23:12Z', Map({'starts_on': Date()}))
