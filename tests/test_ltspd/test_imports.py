"""Every module in the package imports cleanly"""

from importlib import import_module
from pkgutil import walk_packages

import pytest

import ltspd

MODULES = [m.name for m in walk_packages(ltspd.__path__, "ltspd.")]


@pytest.mark.parametrize("module", MODULES)
def test_import(module):
    import_module(module)
