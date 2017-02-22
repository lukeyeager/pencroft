from __future__ import absolute_import

import multiprocessing
import os
import tarfile
import zipfile


# Need a global variable instead of a class variable to avoid errors like:
#   > RuntimeError: Synchronized objects should only be shared between
#     processes through inheritance
# Need an array instead of a single object in order to support multiple
# synchronized Loaders in the same program.
synch_iter_counters_lock = multiprocessing.Lock()  # protects list
synch_iter_counters = []  # list of (Value, Lock) tuples


class Loader(object):
    """Generic loader class"""

    @classmethod
    def new(cls, path):
        """Utility function for auto-detecting the type of PATH
        and returning an instance of the appropriate class.
        """
        from .folder import FolderLoader
        from .tarfile import TarfileLoader
        from .zipfile import ZipfileLoader

        path = os.path.realpath(path)
        if not os.path.exists(path):
            open(path, 'r')  # raise standard exception
        elif os.path.isfile(path):
            if tarfile.is_tarfile(path):
                return TarfileLoader(path)
            elif zipfile.is_zipfile(path):
                return ZipfileLoader(path)
        elif os.path.isdir(path):
            return FolderLoader(path)
        raise ValueError("Couldn't infer type of \"%s\"" % path)

    def __init__(self, path):
        if type(self) == Loader:
            raise ValueError("Don't instantiate Loader directly. "
                             "Use Loader.new() instead.")
        self.path = os.path.realpath(path)

        with synch_iter_counters_lock:
            self._synch_iter_index = len(synch_iter_counters)
            synch_iter_counters.append(
                (
                    multiprocessing.Lock(),
                    multiprocessing.Value('l'),  # signed long
                )
            )

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        """Returns the next (key, data) tuple."""
        keys = self.keys()
        index = -1
        lock, value = synch_iter_counters[self._synch_iter_index]
        with lock:
            if value.value < len(keys):
                index = value.value
                value.value += 1
        if index != -1:
            key = keys[index]
            data = self.get(key)
            return key, data
        else:
            raise StopIteration()

    def keys(self):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def reset(self, randomize_keys=False):
        raise NotImplementedError

    def _reset_iter(self):
        lock, value = synch_iter_counters[self._synch_iter_index]
        with lock:
            value.value = 0
