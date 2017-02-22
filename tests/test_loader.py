import sys

PY3 = sys.version_info[0] == 3


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
