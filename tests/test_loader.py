import multiprocessing.pool
import sys

PY3 = sys.version_info[0] == 3


# Used in a multiprocessing test
# Must be defined at the module level
def _add_next_len(loader, queue):
    for data in loader:
        queue.put(len(data))


class TestLoader:
    """Generic loader tests, should pass for all loaders"""

    def test_keys(self, mytest_loader, mytest_keys):
        assert sorted(mytest_keys) == sorted(mytest_loader.keys())

    def test_exists(self, mytest_loader):
        key = mytest_loader.keys()[-1]
        assert mytest_loader.exists(key)

    def test_get(self, mytest_loader):
        key = mytest_loader.keys()[-1]
        data = mytest_loader.get(key)
        if PY3:
            assert isinstance(data, bytes)
        else:
            assert isinstance(data, str)

    def test_iter(self, mytest_loader):
        data = next(mytest_loader)
        if PY3:
            assert isinstance(data, bytes)
        else:
            assert isinstance(data, str)

    def test_multithreaded_iter(self, mytest_loader, mytest_keys):
        """When multiple threads are calling next(loader) in parallel,
        each key should only be used once."""
        q = multiprocessing.Queue()
        t1 = multiprocessing.Process(
            target=_add_next_len,
            args=(mytest_loader, q),
        )
        t2 = multiprocessing.Process(
            target=_add_next_len,
            args=(mytest_loader, q),
        )
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert q.qsize() == len(mytest_keys)
