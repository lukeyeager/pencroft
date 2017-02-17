from __future__ import (
    absolute_import,
    print_function,
)

import random
import time

from . import open as open_path


class _Timer(object):
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        print('%40s: %f' % (self.message, time.time() - self.start))


def main(args):
    path = args.path
    print('Benchmarking performance on "%s" ...' % path)

    with _Timer('Total'):
        with _Timer('Initialization'):
            loader = open_path(path)

        with _Timer('Read keys'):
            keys = loader.keys()

        random.shuffle(keys)

        with _Timer('Read values'):
            for key in keys:
                loader.get(key)
