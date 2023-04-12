import json
import os
from typing import Any


ENV_KEY = 'JG_GLOBAL_STATE'


def load(env_key=None) -> dict:
    try:
        return json.loads(os.environ[env_key or ENV_KEY])
    except KeyError:
        return dict()


def save(state, env_key=None) -> None:
    os.environ[env_key or ENV_KEY] = json.dumps(state)


def set(name, value, **kwargs) -> None:
    data = load(**kwargs)
    data[name] = value
    save(data, **kwargs)


def get(*args, **kwargs) -> Any:
    return load(**kwargs).get(*args)
