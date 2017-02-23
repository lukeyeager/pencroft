from __future__ import absolute_import

import os
import tarfile
import zipfile

from .loaders.loader import Loader
from .loaders.folder import FolderLoader
from .loaders.tarfile import TarfileLoader
from .loaders.zipfile import ZipfileLoader

from .monkey import patch_pickle

patch_pickle()

__all__ = [
    'open',
    'Loader',
    'FolderLoader',
    'TarfileLoader',
    'ZipfileLoader',
]


def open(path):
    """Auto-detects the type of PATH and returns an instance of the
    appropriate class."""
    path = os.path.realpath(path)
    if not os.path.exists(path):
        raise IOError("No such file or directory: '%s'" % path)
    elif os.path.isfile(path):
        if tarfile.is_tarfile(path):
            return TarfileLoader(path)
        elif zipfile.is_zipfile(path):
            return ZipfileLoader(path)
    elif os.path.isdir(path):
        return FolderLoader(path)
    raise ValueError("Couldn't infer type of \"%s\"" % path)
