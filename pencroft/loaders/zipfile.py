from __future__ import absolute_import

import zipfile


class ZipfileLoader(object):
    """Loads from a zipfile.

    Cannot currently be used in conjunction with multiprocessing.
    To do it, we'd have to re-open the file in each process.
    """
    def __init__(self, path):
        self.file = zipfile.ZipFile(path)
        self._names_to_info = None

    def _set_names_to_info(self):
        assert self._names_to_info is None
        self._names_to_info = dict(
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
        return self.file.read(info)
