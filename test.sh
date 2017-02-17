#!/bin/bash
set -e

flush_caches ()
{
    sync && echo 'echo 3 > /proc/sys/vm/drop_caches' | sudo sh
}
FOLDER=${FOLDER:-/raid/images/mnist/test}
TARFILE=${TARFILE:-/raid/images/mnist/tar-sorted/test.tar}

flush_caches
python -m archive_vfs benchmark ${FOLDER}

flush_caches
python -m archive_vfs benchmark ${FOLDER} -t 4 -l threading

flush_caches
python -m archive_vfs benchmark ${FOLDER} -t 4 -l multiprocessing

flush_caches
python -m archive_vfs benchmark ${TARFILE}

flush_caches
python -m archive_vfs benchmark ${TARFILE} -t 4 -l threading
