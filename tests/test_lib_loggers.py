import pytest

from jg.coop.lib import loggers


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            "/a/b/c/juniorguru/src/jg/coop/sync/club_content/__init__.py",
            "jg.coop.sync.club_content",
        ),
        (
            "/a/b/c/juniorguru/src/jg/coop/sync/club_content/crawler.py",
            "jg.coop.sync.club_content.crawler",
        ),
    ],
)
def test_from_path(path, expected):
    assert loggers.from_path(path, cwd="/a/b/c/juniorguru").name == expected


@pytest.mark.parametrize(
    "key, expected",
    [
        (123, "name.123"),
        ("abc", "name.abc"),
    ],
)
def test_getitem(key, expected):
    assert loggers.get("name")[key].name == expected


@pytest.mark.parametrize(
    "process_name, expected",
    [
        ("MainProcess", ""),
        ("SpawnPoolWorker-1", "/worker1"),
        ("ForkPoolWorker-2", "/worker2"),
        ("Process-3", "/process3"),
    ],
)
def test_get_process_suffix(process_name, expected):
    assert loggers._get_process_suffix(process_name) == expected


@pytest.mark.parametrize(
    "global_value, env, expected",
    [
        (None, {}, "INFO"),
        ("", {}, "INFO"),
        (None, {"LOG_LEVEL": ""}, "INFO"),
        ("debug", {}, "DEBUG"),
        (None, {"LOG_LEVEL": "debug"}, "DEBUG"),
    ],
)
def test_infer_level(global_value, env, expected):
    assert loggers._infer_level(global_value, env) == expected


@pytest.mark.parametrize(
    "global_value, env, expected",
    [
        (None, {}, False),
        ("", {}, False),
        ("false", {}, False),
        (None, {"LOG_TIMESTAMP": ""}, False),
        (None, {"LOG_TIMESTAMP": "", "CI": ""}, False),
        (None, {"LOG_TIMESTAMP": "false"}, False),
        (None, {"CI": "false"}, False),
        (None, {"LOG_TIMESTAMP": "False"}, False),
        (None, {"CI": "False"}, False),
        (None, {"LOG_TIMESTAMP": "0"}, False),
        (None, {"CI": "0"}, False),
        (None, {"LOG_TIMESTAMP": "false", "CI": "true"}, False),
        (None, {"LOG_TIMESTAMP": "true", "CI": "false"}, True),
        ("true", {"LOG_TIMESTAMP": "false", "CI": "false"}, True),
        ("true", {}, True),
        (None, {"CI": "true"}, True),
    ],
)
def test_infer_timestamp(global_value, env, expected):
    assert loggers._infer_timestamp(global_value, env) is expected
