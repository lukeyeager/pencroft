from __future__ import absolute_import

from .loaders.loader import Loader
from .loaders.folder import FolderLoader
from .loaders.tarfile import TarfileLoader
from .loaders.zipfile import ZipfileLoader

from .monkey import patch_pickle

patch_pickle()

__all__ = [
    'Loader',
    'FolderLoader',
    'TarfileLoader',
    'ZipfileLoader',
]
