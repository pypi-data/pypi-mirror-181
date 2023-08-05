"""A simple wrapper around IPython Kernel"""


from .kernel import DummyKernel

from . import _version

__version__ = _version.get_versions()["version"]
