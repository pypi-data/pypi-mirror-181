import pathlib
from typing import Union
from pathlib import Path


def get_path_absolute(path: Union[str, Path]) -> Path:
    """
    获取文件的绝对路径

    Args:
        path: 文件路径, 相对路径或绝对路径

    Returns: 绝对路径

    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    if not path.exists():
        raise RuntimeError(f"{path} is not exists.")

    if not path.is_absolute():
        path = path.absolute()

    return path
