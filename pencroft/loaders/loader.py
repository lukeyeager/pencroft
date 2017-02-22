from __future__ import absolute_import

import os
import tarfile
import zipfile


class Loader(object):
    """Generic loader class"""

    @classmethod
    def new(cls, path):
        """Utility function for auto-detecting the type of PATH
        and returning an instance of the appropriate class.
        """
        from .folder import FolderLoader
        from .tarfile import TarfileLoader
        from .zipfile import ZipfileLoader

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

    def __init__(self, path):
        if type(self) == Loader:
            raise ValueError("Don't instantiate Loader directly. "
                             "Use Loader.new() instead.")
        self.path = os.path.realpath(path)
        self._iter_n = 0

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        keys = self.keys()
        if self._iter_n < len(keys):
            data = self.get(keys[self._iter_n])
            self._iter_n += 1
            return data
        else:
            self._iter_n = 0
            raise StopIteration()

    def keys(self):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError
