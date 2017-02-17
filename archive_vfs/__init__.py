from __future__ import absolute_import

import os.path

from .loaders.folder import FolderLoader
from .loaders.tarfile import TarfileLoader


def open(path):
    path = os.path.realpath(path)
    if os.path.isfile(path):
        return TarfileLoader(path)
    elif os.path.isdir(path):
        return FolderLoader(path)
    else:
        raise ValueError("Couldn't infer type of \"%s\"" % path)
