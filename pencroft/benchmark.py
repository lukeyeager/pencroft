from __future__ import absolute_import

import functools
import random
import time

from . import Loader


def set_parser(parser):
    parser.add_argument('path')
    parser.add_argument('-t', '--threads', type=int, default=1)
    parser.add_argument('-l', '--thread-library', default='threading',
                        choices=['threading', 'multiprocessing'])
    parser.set_defaults(func=main)


class _Timer(object):
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        print('%20s: %f' % (self.message, time.time() - self.start))


def get_data(loader, key):
    data = loader.get(key)
    return len(data)


def benchmark(path, threads=1, thread_library='threading'):
    print('%20s: %s' % ('File', path))
    print('%20s: %d' % ('Threads', threads))
    if threads > 1:
        print('%20s: %s' % ('Library', thread_library))

    if threads > 1:
        import multiprocessing.pool
        if thread_library == 'threading':
            pool = multiprocessing.pool.ThreadPool(threads)
        elif thread_library == 'multiprocessing':
            pool = multiprocessing.pool.Pool(threads)

    with _Timer('Total'):
        with _Timer('Initialization'):
            loader = Loader(path)

        with _Timer('Read keys'):
            keys = loader.keys()

        random.shuffle(keys)

        with _Timer('Read data'):
            if threads > 1:
                pool.map(functools.partial(get_data, loader), keys)
            else:
                for key in keys:
                    loader.get(key)
    print()


def main(args):
    benchmark(args.path,
              threads=args.threads,
              thread_library=args.thread_library)
