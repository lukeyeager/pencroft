from pencroft import ZipfileLoader


def test_keys(mytest_zipfile, mytest_keys):
    loader = ZipfileLoader(mytest_zipfile)
    assert sorted(mytest_keys) == sorted(loader.keys())


def test_get(mytest_zipfile):
    loader = ZipfileLoader(mytest_zipfile)
    keys = loader.keys()
    for key in keys:
        loader.get(key)
