from . import models
from . import api
from .models.datasource.datawrapper import FileDataWrapper, GcsDataWrapper, S3DataWrapper
from .models.datasource.datawrapper.metadata import DatasetSourceUsage
from .models.model import Model
from .models.git_version import CodeSource

from vectice.connection import Connection
from .__version__ import __version__

from vectice.utils.logging_utils import _configure_vectice_loggers, disable_logging


connect = Connection.connect

_configure_vectice_loggers(root_module_name=__name__)
silent = disable_logging

version = __version__

__all__ = [
    "api",
    "models",
    "version",
    "connect",
    "FileDataWrapper",
    "GcsDataWrapper",
    "S3DataWrapper",
    "DatasetSourceUsage",
    "silent",
    "Model",
    "CodeSource",
]
