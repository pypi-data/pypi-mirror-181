from pathlib import Path
from jinja2.loaders import FileSystemLoader
from jinja2.environment import Environment
from lowcode_cli.conf.settings import settings


def create_default_loader(tpl_file: Path):
    loader = FileSystemLoader(tpl_file.parent)
    return loader


def create_default_env(tpl_file: Path):
    loader = create_default_loader(tpl_file)
    env = Environment(loader=loader)

    variable_start_string = settings.get("jinja2.variable_start_string", "{%")
    variable_end_string = settings.get("jinja2.variable_end_string", "%}")
    if variable_end_string and variable_start_string:
        env.variable_start_string = variable_start_string
        env.variable_end_string = variable_end_string

    return env
