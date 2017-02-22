from __future__ import absolute_import

import tarfile

from .loader import Loader


class TarfileLoader(Loader):
    """Loads from a tarfile"""

    def __init__(self, *args, **kwargs):
        super(TarfileLoader, self).__init__(*args, **kwargs)
        self._names_to_members = None

    def __getstate__(self):
        """Used for pickling (which is used by multiprocessing)"""
        d = self.__dict__.copy()
        d.pop('_file', None)  # not pickle-able
        return d

    @property
    def file(self):
        """Lazy loading property - helps with multi-processing"""
        try:
            return self._file
        except AttributeError:
            self._file = tarfile.open(self.path)
            return self._file

    def _set_names_to_members(self):
        assert self._names_to_members is None
        self._names_to_members = dict(
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
        try:
            return self.file.extractfile(member).read()
        except ValueError:
            # Try re-opening the file
            self.file = tarfile.open(self.path)
            return self.file.extractfile(member).read()
