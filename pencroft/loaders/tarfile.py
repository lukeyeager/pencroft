from __future__ import absolute_import

from collections import OrderedDict
import tarfile

from .loader import Loader


class TarfileLoader(Loader):
    """Loads from a tarfile"""

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_file', None)  # not pickle-able
        return d

    def _open_file(self):
        self._file = tarfile.open(self.path)

    @property
    def file(self):
        try:
            return self._file
        except AttributeError:
            self._open_file()
            return self._file

    def _set_keys(self):
        self._names_to_members = OrderedDict(
            [(m.name, m) for m in self.file.getmembers() if m.isfile()])
        self._keys = list(self._names_to_members.keys())

    def get(self, key):
        member = self._names_to_members[key]
        with self._lock:
            try:
                return self.file.extractfile(member).read()
            except ValueError:
                # Try re-opening the file
                self._open_file()
                return self.file.extractfile(member).read()
