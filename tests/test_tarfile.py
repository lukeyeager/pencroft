from pencroft import TarfileLoader


def test_keys(mytest_tarfile, mytest_keys):
    loader = TarfileLoader(mytest_tarfile)
    assert sorted(mytest_keys) == sorted(loader.keys())


def test_get(mytest_tarfile):
    loader = TarfileLoader(mytest_tarfile)
    keys = loader.keys()
    for key in keys:
        loader.get(key)
