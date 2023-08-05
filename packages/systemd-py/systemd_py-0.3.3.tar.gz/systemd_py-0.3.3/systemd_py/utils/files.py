from typing import Union
from pathlib import Path


def get_file(name: str, path: Union[str, Path]) -> Path:
    """
    Validate path
    """

    if not name.endswith('.service'):
        name += '.service'

    if isinstance(path, str):
        path = Path(path)

    path = path.resolve()

    if path.is_file():
        path = path.parent

    return path / name
