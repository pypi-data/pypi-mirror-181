from pathlib import Path
from typing import Union
from lowcode_cli.core.renderer import FileRenderer, DirRenderer


def render_file(tpl_file: Union[str, Path], schema_file: Path):
    if isinstance(tpl_file, str):
        tpl_file = Path(tpl_file)
    renderer = FileRenderer()
    return renderer.render(tpl_file, schema_file)


def render_dir(tpl_dir: Union[str, Path], output=None):
    if isinstance(tpl_dir, str):
        tpl_dir = Path(tpl_dir)
    if isinstance(output, str):
        output = Path(output)
    renderer = DirRenderer(tpl_dir, output)
    return renderer.render()
