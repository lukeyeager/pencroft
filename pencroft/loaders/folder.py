from __future__ import absolute_import

import os

from .loader import Loader


class FolderLoader(Loader):

    def _set_keys(self):
        self._keys = []
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                self._keys.append(os.path.relpath(
                    os.path.join(dirpath, filename),
                    self.path,
                ))

    def get(self, key):
        if os.path.isabs(key):
            raise ValueError('Path must be relative to root, not absolute')
        path = os.path.join(self.path, key)
        if not os.path.commonprefix([path, self.path]).startswith(self.path):
            raise ValueError('"%s" is not in "%s"' % (path, self.path))
        with open(path, 'rb') as infile:
            return infile.read()
