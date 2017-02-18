import pytest

from pencroft.benchmark import main


class Args(object):
    pass


def test_folder_1(mytest_folder):
    args = Args()
    args.path = mytest_folder
    args.threads = 1
    main(args)


def test_folder_4thread(mytest_folder):
    args = Args()
    args.path = mytest_folder
    args.threads = 4
    args.thread_library = 'threading'
    main(args)


def test_folder_4proc(mytest_folder):
    args = Args()
    args.path = mytest_folder
    args.threads = 4
    args.thread_library = 'multiprocessing'
    main(args)


def test_tarfile_1(mytest_tarfile):
    args = Args()
    args.path = mytest_tarfile
    args.threads = 1
    main(args)


def test_tarfile_4thread(mytest_tarfile):
    args = Args()
    args.path = mytest_tarfile
    args.threads = 4
    args.thread_library = 'threading'
    main(args)


@pytest.mark.xfail
def test_tarfile_4proc(mytest_tarfile):
    args = Args()
    args.path = mytest_tarfile
    args.threads = 4
    args.thread_library = 'multiprocessing'
    main(args)
