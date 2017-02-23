import itertools
import os
import shutil
import tarfile
import tempfile
import zipfile

import pencroft
import pytest


@pytest.fixture(scope='session')
def mytest_keys():
    x = {'a', 'b', 'c', 'foo', 'bar', 'baz'}
    return sorted({os.path.sep.join(p) for p in itertools.permutations(x)})


@pytest.fixture(scope='session')
def mytest_folder(mytest_keys):
    d = tempfile.mkdtemp()
    for key in mytest_keys:
        dirname, filename = os.path.split(key)
        if dirname:
            os.makedirs(os.path.join(d, dirname))
        with open(os.path.join(d, key), 'wb') as outfile:
            # More than 1 page
            outfile.write(os.urandom(5000))
    yield d
    shutil.rmtree(d)


@pytest.fixture(scope='session')
def mytest_tarfile(mytest_folder):
    filehandle, filename = tempfile.mkstemp(suffix='.tar')
    os.close(filehandle)
    os.remove(filename)
    tf = tarfile.open(filename, 'w')
    tf.add(mytest_folder, arcname='')
    tf.close()
    yield filename
    os.remove(filename)


@pytest.fixture(scope='session')
def mytest_zipfile(mytest_folder):
    filehandle, filename = tempfile.mkstemp(suffix='.zip')
    os.close(filehandle)
    os.remove(filename)
    zf = zipfile.ZipFile(filename, 'w')
    for dirpath, dirnames, filenames in os.walk(mytest_folder):
        for path in filenames:
            path = os.path.join(dirpath, path)
            arcname = os.path.relpath(path, mytest_folder)
            zf.write(path, arcname=arcname)
    zf.close()
    yield filename
    os.remove(filename)


@pytest.fixture(params=['folder', 'tarfile', 'zipfile'])
def mytest_path(request, mytest_folder, mytest_tarfile, mytest_zipfile):
    t = request.param
    if t == 'folder':
        return mytest_folder
    if t == 'tarfile':
        return mytest_tarfile
    if t == 'zipfile':
        return mytest_zipfile
    assert False, 'Should not reach here'


@pytest.fixture(params=['folder', 'tarfile', 'zipfile'])
def mytest_loader(request, mytest_folder, mytest_tarfile, mytest_zipfile):
    t = request.param
    if t == 'folder':
        return pencroft.FolderLoader(mytest_folder)
    if t == 'tarfile':
        return pencroft.TarfileLoader(mytest_tarfile)
    if t == 'zipfile':
        return pencroft.ZipfileLoader(mytest_zipfile)
    assert False, 'Should not reach here'
