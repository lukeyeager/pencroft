from __future__ import absolute_import

from collections import OrderedDict
import zipfile

from .loader import Loader


class ZipfileLoader(Loader):
    """Loads from a zipfile"""

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

    def _set_keys(self):
        self._names_to_info = OrderedDict(
            [(i.filename, i) for i in self.file.infolist()])
        self._keys = list(self._names_to_info.keys())

    def get(self, key):
        info = self._names_to_info[key]
        with self._lock:
            return self.file.read(info)
