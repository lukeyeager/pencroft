from __future__ import absolute_import

import ctypes
import multiprocessing
import os
import tarfile
import threading
import zipfile


class NoopLock(object):
    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        pass

    def acquire(self, *args, **kwargs):
        return False


class Loader(object):
    """Generic loader class"""

    @classmethod
    def new(cls, path, *args, **kwargs):
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
                return TarfileLoader(path, *args, **kwargs)
            elif zipfile.is_zipfile(path):
                return ZipfileLoader(path, *args, **kwargs)
        elif os.path.isdir(path):
            return FolderLoader(path, *args, **kwargs)
        raise ValueError("Couldn't infer type of \"%s\"" % path)

    def __init__(self, path, thread_safe=False, mp_safe=False):
        if type(self) == Loader:
            raise ValueError("Don't instantiate Loader directly. "
                             "Use Loader.new() instead.")
        self.path = os.path.realpath(path)
        self._lock = NoopLock()
        self._iter_count = ctypes.c_long(0)
        if mp_safe:
            self.make_mp_safe()
        elif thread_safe:
            self.make_thread_safe()

    def make_mp_safe(self):
        old_lock = self._lock
        with old_lock:
            manager = multiprocessing.Manager()
            self._lock = manager.Lock()
            self._iter_count = manager.Value('l', self._iter_count.value)

    def make_thread_safe(self):
        old_lock = self._lock
        with old_lock:
            self._lock = threading.Lock()
            self._iter_count = ctypes.c_long(self._iter_count.value)

    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next (key, data) tuple."""
        key = None
        with self._lock:
            keys = self.keys()
            if self._iter_count.value < len(keys):
                key = keys[self._iter_count.value]
                self._iter_count.value += 1
            else:
                raise StopIteration()
        data = self.get(key)
        return (key, data)

    # Python 2 compatibility
    def next(self):
        return self.__next__()

    def set_lock(self, lock):
        self._lock = lock

    def keys(self):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def reset(self, shuffle_keys=False):
        raise NotImplementedError

    def _reset_iter(self):
        assert not self._lock.acquire(block=False), \
            'Must acquire lock before calling _reset_iter()'
        self._iter_count.value = 0
