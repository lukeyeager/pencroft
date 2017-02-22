from __future__ import absolute_import

from .loaders.loader import Loader
from .loaders.folder import FolderLoader
from .loaders.tarfile import TarfileLoader
from .loaders.zipfile import ZipfileLoader

__all__ = [
    'Loader',
    'FolderLoader',
    'TarfileLoader',
    'ZipfileLoader',
]
