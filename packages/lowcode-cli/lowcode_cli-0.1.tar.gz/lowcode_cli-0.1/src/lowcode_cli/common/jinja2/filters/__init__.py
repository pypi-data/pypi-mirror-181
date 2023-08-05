from jinja2.environment import Environment
from typing import Callable, Iterable
from lowcode_cli.conf.settings import settings

FILTER_PREFIX = settings.get("FILTER_PREFIX", "__filter__")


def register_filters(env: Environment, filters: Iterable[Callable]):
    for filter_ in filters:
        filter_name = getattr(filter_, "__name__")
        env.filters[f"{FILTER_PREFIX}.{filter_name}"] = filter_
