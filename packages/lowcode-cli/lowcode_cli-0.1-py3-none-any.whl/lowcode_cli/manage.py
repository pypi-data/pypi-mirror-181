import click
from lowcode_cli.conf.settings import settings
from pathlib import Path
from lowcode_cli.core.commands import render

BASE_DIR = settings["BASE_DIR"]


@click.group()
def cli():
    ...


@click.command()
@click.option("--schema-file", "-sf", help="请选择jsonschema文件路径.")
@click.option("--tpl-file", "-tf", help="请选择jinja2模板文件路径.")
@click.option("--save-file", required=False, help="保存路径, 若False, 输出到终端.")
def render_file(tpl_file: str, schema_file: str, save_file: str = None):
    """
    根据schema_file渲染单个模板文件

    Args:
        save_file: 保存路径, 非必填, 若False则输出到终端
        tpl_file: 模板文件, 支持相对路径和绝对路径
        schema_file: schema文件, 支持相对路径和绝对路径

    Returns:
        nothing

    """

    tpl_file = Path(tpl_file)
    if not tpl_file.is_absolute():
        tpl_file = tpl_file.absolute()

    schema_file = Path(schema_file)
    if not schema_file.is_absolute():
        schema_file = schema_file.absolute()

    if save_file:
        save_file = Path(save_file)
        if not save_file.is_absolute():
            save_file = save_file.absolute()

    content = render.render_file(tpl_file, schema_file)
    if save_file:
        save_file.write_text(content)
    else:
        print(content)


@click.command()
@click.option(
    "--tpl_dir",
    "-d",
    "--tpl-dir",
    required=True,
    type=str,
    help="请选择jinja2模板文件目录, 将自动根据同文件名schema后缀的json文件渲染.",
)
@click.option("--output", "-o", required=False, type=str, help="写入到指定目录.")
def render_dir(tpl_dir: str, output: str):
    """
    遍历tpl_dir目录, **/*.tpl和**/*.json配对渲染

    Args:
        output: 写入到指定目录
        tpl_dir: 模板目录

    Returns:
        nothing

    """
    tpl_dir = Path(tpl_dir)

    if not tpl_dir.exists():
        click.echo("template dir is not exists.")
        return

    render.render_dir(tpl_dir, output)


cli.add_command(render_file)
cli.add_command(render_dir)

if __name__ == "__main__":
    cli()
