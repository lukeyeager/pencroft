from pencroft import FolderLoader


def test_keys(mytest_folder, mytest_keys):
    loader = FolderLoader(mytest_folder)
    assert sorted(mytest_keys) == sorted(loader.keys())


def test_get(mytest_folder):
    loader = FolderLoader(mytest_folder)
    keys = loader.keys()
    for key in keys:
        loader.get(key)
