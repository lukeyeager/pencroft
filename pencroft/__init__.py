from __future__ import absolute_import

import os.path
import tarfile
import zipfile

from .loaders.folder import FolderLoader
from .loaders.tarfile import TarfileLoader
from .loaders.zipfile import ZipfileLoader


def Loader(path):
    """Returns a Loader of the appropriate type"""
    path = os.path.realpath(path)
    if not os.path.exists(path):
        open(path, 'r')  # raise standard exception
    elif os.path.isfile(path):
        if tarfile.is_tarfile(path):
            return TarfileLoader(path)
        elif zipfile.is_zipfile(path):
            return ZipfileLoader(path)
    elif os.path.isdir(path):
        return FolderLoader(path)
    raise ValueError("Couldn't infer type of \"%s\"" % path)
