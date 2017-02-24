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
./examples/pytorch/main.py "$FOLDER" --workers=10 --pytorch_loader
clear-caches
./examples/pytorch/main.py "$FOLDER" --workers=10
clear-caches
./examples/pytorch/main.py "$TARFILE" --workers=10

# resnet-50

clear-caches
./examples/pytorch/main.py "$FOLDER" --workers=10 --use_resnet50 --pytorch_loader
clear-caches
./examples/pytorch/main.py "$FOLDER" --workers=10 --use_resnet50
clear-caches
./examples/pytorch/main.py "$TARFILE" --workers=10 --use_resnet50
