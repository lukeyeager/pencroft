from __future__ import absolute_import

from collections import OrderedDict
import random
import zipfile

from .loader import Loader


class ZipfileLoader(Loader):
    """Loads from a zipfile"""

    def __init__(self, *args, **kwargs):
        super(ZipfileLoader, self).__init__(*args, **kwargs)
        self._names_to_info = None

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_file', None)  # not pickle-able
        return d

    def _open_file(self):
        self._file = zipfile.ZipFile(self.path)

    @property
    def file(self):
        try:
            return self._file
        except AttributeError:
            self._open_file()
            return self._file

    def _set_names_to_info(self):
        assert self._names_to_info is None
        self._names_to_info = OrderedDict(
            [(i.filename, i) for i in self.file.infolist()])

    def keys(self):
        if self._names_to_info is None:
            self._set_names_to_info()
        return list(self._names_to_info.keys())

    def exists(self, key):
        if self._names_to_info is None:
            self._set_names_to_info()
        return key in self._names_to_info

    def get(self, key):
        info = self._names_to_info[key]
        with self._lock:
            return self.file.read(info)

    def reset(self, shuffle_keys=False):
        with self._lock:
            super(ZipfileLoader, self)._reset_iter()
            if shuffle_keys:
                items = self._names_to_info
                random.shuffle(items)
                self._names_to_info = OrderedDict(items)
