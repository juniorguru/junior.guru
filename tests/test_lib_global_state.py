import os
from time import perf_counter_ns

import pytest

from project.lib.global_state import get, load, save, set


@pytest.fixture
def env_key():
    env = os.environ.copy()
    try:
        yield f"JG_GLOBAL_STATE_TEST_{perf_counter_ns()}"
    finally:
        os.environ.clear()
        os.environ.update(env)


def test_load(env_key: str):
    os.environ[env_key] = '{"foo": "bar"}'

    assert load(env_key=env_key) == {"foo": "bar"}


def test_load_empty(env_key: str):
    assert load(env_key=env_key) == {}


def test_save(env_key: str):
    save({"foo": "bar"}, env_key=env_key)

    assert os.environ[env_key] == '{"foo": "bar"}'


def test_set(env_key: str):
    set("foo", "bar", env_key=env_key)

    assert os.environ[env_key] == '{"foo": "bar"}'


def test_get(env_key: str):
    os.environ[env_key] = '{"foo": "bar"}'

    assert get("foo", env_key=env_key) == "bar"


def test_get_none(env_key: str):
    os.environ[env_key] = '{"foo": "bar"}'

    assert get("baz", env_key=env_key) is None


def test_get_default(env_key: str):
    os.environ[env_key] = '{"foo": "bar"}'

    assert get("baz", "qux", env_key=env_key) == "qux"
