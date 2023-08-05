from jinja2.environment import Environment
from typing import Callable, Iterable
from lowcode_cli.conf.settings import settings

HANDLE_PREFIX = settings.get("FILTER_PREFIX", "__handle__")


def register_handles(env: Environment, handles: Iterable[Callable]):
    for handle in handles:
        handle_name = getattr(handle, "__name__")
        env.filters[f"${HANDLE_PREFIX}.{handle_name}"] = handle
