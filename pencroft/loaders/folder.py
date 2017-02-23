from __future__ import absolute_import

import os
import random

from .loader import Loader


class FolderLoader(Loader):

    def __init__(self, *args, **kwargs):
        super(FolderLoader, self).__init__(*args, **kwargs)
        self._filenames = None

    def _set_filenames(self):
        assert self._filenames is None
        self._filenames = []
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                self._filenames.append(os.path.relpath(
                    os.path.join(dirpath, filename),
                    self.path,
                ))

    def keys(self):
        if self._filenames is None:
            self._set_filenames()
        return self._filenames

    def exists(self, key):
        return key in self._filenames

    def get(self, key):
        if os.path.isabs(key):
            raise ValueError('Path must be relative to root, not absolute')
        path = os.path.join(self.path, key)
        if not os.path.commonprefix([path, self.path]).startswith(self.path):
            raise ValueError('"%s" is not in "%s"' % (path, self.path))
        with open(path, 'rb') as infile:
            return infile.read()

    def reset(self, shuffle_keys=False):
        with self._lock:
            super(FolderLoader, self)._reset_iter()
            if shuffle_keys:
                random.shuffle(self._filenames)
