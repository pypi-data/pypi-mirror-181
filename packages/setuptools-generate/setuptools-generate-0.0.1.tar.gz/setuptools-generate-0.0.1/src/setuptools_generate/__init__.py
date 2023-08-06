"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
import logging
import os
import sys
from importlib import import_module
from typing import Callable

from click import BaseCommand
from setuptools import Distribution

from ._help2man import generate_man
from ._version import __version__, __version_tuple__  # type: ignore

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

logger = logging.getLogger(__name__)


def generate(distribution: Distribution | None = None) -> None:
    """Generate.

    :param distribution:
    :type distribution: Distribution | None
    :rtype: None
    """
    if not os.path.isfile("pyproject.toml"):
        logger.error("No pyproject.toml is found!")
        return
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    try:
        write_to: str = data["tool"]["setuptools-generate"]["write-to"]

        from .metainfo import generate_metainfo  # isort: skip

        generate_metainfo(write_to, data)
    except KeyError:
        logger.warning(
            "no [tool.setuptools-generate.write-to] in pyproject.toml, "
            "skip writing metainfo!"
        )
    try:
        completions: dict[str, str] = data["project"]["scripts"]
    except KeyError:
        logger.warning("No [project.scripts] in your pyproject.toml!")
        return
    cwd = os.getcwd()
    resources = os.path.join(os.path.join(cwd, "build"), "resources")
    os.makedirs(resources, exist_ok=True)
    sys.path.insert(0, cwd)
    sys.path.insert(0, os.path.join(cwd, "src"))
    for prog, path in completions.items():
        module_path, _, function_name = path.rpartition(":")
        module = import_module(module_path)
        function = vars(module).get(function_name)
        if isinstance(function, BaseCommand):
            from ._click import generate_complete
        elif isinstance(function, Callable):
            from ._shtab import generate_complete
        else:
            logger.error(path + " cannot be called!")
            return

        generate_complete(function, prog, resources)  # type: ignore
        generate_man(function, prog, resources, data)
    sys.path.pop(0)
    sys.path.pop(0)
