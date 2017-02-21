import itertools
import os
import shutil
import tarfile
import tempfile
import zipfile

import pytest


@pytest.fixture(scope='session')
def mytest_keys():
    x = {'a', 'b', 'c', 'foo', 'bar', 'baz'}
    return {os.path.sep.join(p) for p in itertools.permutations(x)}


@pytest.fixture(scope='session')
def mytest_folder(mytest_keys):
    d = tempfile.mkdtemp()
    for key in mytest_keys:
        dirname, filename = os.path.split(key)
        if dirname:
            os.makedirs(os.path.join(d, dirname))
        with open(os.path.join(d, key), 'w') as outfile:
            outfile.write('test')
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
