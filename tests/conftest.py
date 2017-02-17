import os
import shutil
import tarfile
import tempfile

import pytest


@pytest.fixture(scope='session')
def mytest_keys():
    return ['foo', 'bar/baz']


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
