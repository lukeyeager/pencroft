import tarfile


class TarfileLoader(object):
    """Loads from a tarfile.

    Cannot currently be used in conjunction with multiprocessing.
    To do it, we'd have to re-open the file in each process.
    """
    def __init__(self, path):
        self.file = tarfile.open(path)
        self._names_to_members = None

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
        return self.file.extractfile(member).read()
