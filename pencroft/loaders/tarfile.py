from __future__ import absolute_import

from collections import OrderedDict
import random
import tarfile

from .loader import Loader


class TarfileLoader(Loader):
    """Loads from a tarfile"""

    def __init__(self, *args, **kwargs):
        super(TarfileLoader, self).__init__(*args, **kwargs)
        self._names_to_members = None

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

    def _set_names_to_members(self):
        assert self._names_to_members is None
        self._names_to_members = OrderedDict(
            [(m.name, m) for m in self.file.getmembers() if m.isfile()])

    def keys(self):
        if self._names_to_members is None:
            self._set_names_to_members()
        return list(self._names_to_members.keys())

    def exists(self, key):
        if self._names_to_members is None:
            self._set_names_to_members()
        return key in self._names_to_members

    def get(self, key):
        member = self._names_to_members[key]
        with self._lock:
            try:
                return self.file.extractfile(member).read()
            except ValueError:
                # Try re-opening the file
                self._open_file()
                return self.file.extractfile(member).read()

    def reset(self, shuffle_keys=False):
        with self._lock:
            super(TarfileLoader, self)._reset_iter()
            if shuffle_keys:
                items = self._names_to_members
                random.shuffle(items)
                self._names_to_members = OrderedDict(items)
