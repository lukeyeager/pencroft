#!/bin/bash
set -e
set -x

FOLDER=${FOLDER:-imagenet-val-sorted/}
TARFILE=${TARFILE:-imagenet-val-sorted.tar}

clear-caches ()
{
    sync && echo "echo 3 > /proc/sys/vm/drop_caches" | sudo sh
}

# no model

clear-caches
python -m pencroft benchmark "$FOLDER" -t 10 -l multiprocessing

clear-caches
python -m pencroft benchmark "$TARFILE" -t 10 -l multiprocessing

# tiny model

clear-caches
./examples/keras/main.py "$FOLDER" --nb_worker=10 --pickle_safe --keras_loader
clear-caches
./examples/keras/main.py "$FOLDER" --nb_worker=10 --pickle_safe
clear-caches
./examples/keras/main.py "$TARFILE" --nb_worker=10 --pickle_safe

# resnet-50

clear-caches
./examples/keras/main.py "$FOLDER" --nb_worker=10 --pickle_safe --use_resnet50 --keras_loader
clear-caches
./examples/keras/main.py "$FOLDER" --nb_worker=10 --pickle_safe --use_resnet50
clear-caches
./examples/keras/main.py "$TARFILE" --nb_worker=10 --pickle_safe --use_resnet50
