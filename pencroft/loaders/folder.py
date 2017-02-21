import os


class FolderLoader(object):
    def __init__(self, path):
        self.root = os.path.realpath(path)

    def _in_root(self, path):
        if os.path.isabs(path):
            if not os.path.commonprefix(
                    [path, self.root]).startswith(self.root):
                raise ValueError('"%s" is not in "%s"' % (path, self.root))
        else:
            path = os.path.join(self.root, path)
        return path

    def keys(self):
        result = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                result.append(os.path.relpath(
                    os.path.join(dirpath, filename),
                    self.root,
                ))
        return result

    def exists(self, key):
        path = self._in_root(key)
        return os.path.exists(path)

    def get(self, key):
        path = self._in_root(key)
        with open(path, 'rb') as infile:
            return infile.read()
