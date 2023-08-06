from pathlib import Path
from typing import Union
import inspect
import os


def rel_to_abs(rel_path: Union[str, Path], parents=0, return_str=True, strict=False):
    """Return absolute path relative to the called file
    args:
        parent: <int> The number of times `f_back` will be calledd.
    """
    currentframe = inspect.currentframe()
    f = currentframe.f_back
    if parents:
        for _ in range(parents):
            f = f.f_back
    current_path = Path(f.f_code.co_filename).parent
    pathlib_path = current_path / rel_path
    pathlib_path = pathlib_path.resolve(strict=strict)
    if return_str:
        return str(pathlib_path)
    else:
        return pathlib_path


def relp(rel_path: Union[str, Path], parents=0, return_str=True, strict=False):
    return rel_to_abs(rel_path, parents, return_str, strict)


def rel_path_join(*paths: Union[str, Path], return_str=True):
    return rel_to_abs(os.path.join(*paths), parents=1, return_str=return_str)


relp.__doc__ = rel_to_abs.__doc__
