import tarfile

# TODO: thread safety


class TarfileLoader(object):
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
