from pathlib import Path
import json
import jsonschema
from lowcode_cli.common.jsonschema.validators import DefaultValidatingDraft7Validator
from lowcode_cli.common.jinja2.filters import register_filters
import os
from lowcode_cli.utils import make_unique_string
from case_convert import camel_case, snake_case
from lowcode_cli.common.jinja2 import create_default_env
from typing import Iterable, Callable
from lowcode_cli.common.jinja2.handles import register_handles
from lowcode_cli.conf.settings import settings

SCHEMA_SUFFIX = settings.get("SCHEMA_SUFFIX", ".json")
TPL_SUFFIX = settings.get("TPL_SUFFIX", ".tpl")


class FileRenderer:
    # 全局filters和handles
    DEFAULT_FILTERS = (
        camel_case,
        snake_case,
    )
    DEFAULT_HANDLES = ()

    def __init__(
        self, filters: Iterable[Callable] = None, handles: Iterable[Callable] = None,
    ):
        self.filters = filters or []
        self.handles = handles or []
        self.filters.extend(self.DEFAULT_FILTERS)
        self.handles.extend(self.DEFAULT_HANDLES)

    def add_filters(self, filters: Iterable[Callable]):
        self.filters.extend(filters)

    def add_handles(self, handles: Iterable[Callable]):
        self.handles.extend(handles)

    def render(self, tpl_file: Path, schema_file: Path):
        env = create_default_env(tpl_file)

        register_filters(env, self.filters)
        register_handles(env, self.handles)
        tpl = env.get_template(tpl_file.name)

        schema = json.loads(schema_file.read_text())
        resolver = jsonschema.RefResolver(f"file://{schema_file.parent}", schema)
        DefaultValidatingDraft7Validator(schema, resolver).validate({})

        content = tpl.render(schema=schema)
        return content


class DirRenderer:
    def __init__(
        self,
        tpl_dir: Path,
        output: Path = None,
        filters: Iterable[Callable] = None,
        handles: Iterable[Callable] = None,
    ):
        self.tpl_dir = tpl_dir
        self.output = (
            output if output else Path.cwd() / ".lowcode" / make_unique_string()
        )
        if filters is None:
            self.filters = []
        if handles is None:
            self.handles = []

        if not self.output.exists():
            self.output.mkdir(parents=True)

        if not self.output.is_absolute():
            self.output = self.output.absolute()

        self.file_renderer = FileRenderer(filters=self.filters, handles=self.handles)

    def add_filters(self, filters: Iterable[Callable]):
        self.filters.extend(filters)
        self.file_renderer.add_filters(self.filters)

    def add_handles(self, handles: Iterable[Callable]):
        self.handles.extend(handles)
        self.file_renderer.add_handles(self.handles)

    def render(self):
        for root, _dirs, files in os.walk(self.tpl_dir):
            root = Path(root)
            for file_ in files:
                tpl_file = root / file_
                if not tpl_file.suffix == TPL_SUFFIX:
                    continue
                schema_file = Path(
                    str(tpl_file).replace(tpl_file.suffix, SCHEMA_SUFFIX)
                )
                if not schema_file.exists():
                    continue
                schema = json.loads(schema_file.read_text())
                suffix = schema.get("_meta", {}).get("suffix", "")
                content = self.file_renderer.render(
                    tpl_file=tpl_file, schema_file=schema_file
                )
                relpath = tpl_file.relative_to(self.tpl_dir)
                file_output = self.output / str(relpath).replace(
                    tpl_file.suffix, suffix
                )
                if not file_output.parent.exists():
                    file_output.parent.mkdir()
                file_output.write_text(content)
                print(f"RUN: =====> create file {file_output} SUCCESS.")
