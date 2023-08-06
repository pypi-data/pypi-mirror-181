"""Test click."""
import os
import shutil
from pathlib import Path

from setuptools_generate import generate

HERE = os.path.dirname(__file__)


def copy(filename: str, target: str = ".") -> None:
    """Copy.

    :param filename:
    :type filename: str
    :param target:
    :type target: str
    :rtype: None
    """
    shutil.copy(os.path.join(HERE, filename), target)


class Test:
    """Test."""

    def test_click(self, tmp_path: Path) -> None:
        """Test click. Check current directory.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("src/pyproject.toml")
        copy("src/demo_click.py")
        generate()
        for file in list(os.walk("build/resources"))[0][-1]:
            with open(os.path.join("build/resources", file)) as f:
                rst = f.read()
            assert rst != ""
