from __future__ import absolute_import

import ctypes
import multiprocessing
import os
import random
import threading


class NoopLock(object):
    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        pass


class Loader(object):
    """Generic loader class"""

    def __init__(self, path):
        if type(self) == Loader:
            raise ValueError("Don't instantiate Loader directly. "
                             "Use Loader.new() instead.")
        self.path = os.path.realpath(path)
        self._lock = NoopLock()
        self._iter_count = ctypes.c_long(0)
        self._set_keys()

    def make_mp_safe(self):
        old_lock = self._lock
        with old_lock:
            manager = multiprocessing.Manager()
            self._lock = manager.Lock()
            self._iter_count = manager.Value('l', self._iter_count.value)
            self._keys = manager.list(self._keys)

    def make_thread_safe(self):
        old_lock = self._lock
        with old_lock:
            self._lock = threading.Lock()
            self._iter_count = ctypes.c_long(self._iter_count.value)
            self._keys = list(self._keys)

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, index):
        key = self._keys[index]
        data = self.get(key)
        return (key, data)

    def __iter__(self):
        return self

    def __next__(self):
        """Returns the next (key, data) tuple."""
        key = None
        with self._lock:
            if self._iter_count.value < len(self._keys):
                key = self._keys[self._iter_count.value]
                self._iter_count.value += 1
            else:
                raise StopIteration()
        data = self.get(key)
        return (key, data)

    # Python 2 compatibility
    def next(self):
        return self.__next__()

    def _set_keys(self):
        raise NotImplementedError

    def keys(self):
        return list(self._keys)

    def exists(self, key):
        return key in self._keys

    def get(self, key):
        raise NotImplementedError

    def reset(self, shuffle_keys=False):
        with self._lock:
            self._iter_count.value = 0
            if shuffle_keys:
                random.shuffle(self._keys)
