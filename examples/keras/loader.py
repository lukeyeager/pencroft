from cStringIO import StringIO
import os
import random

import numpy as np
import pencroft
import PIL.Image


class Loader(object):
    """Opens SOURCE with pencroft. SOURCE is interpreted as folders named for
    classes containing images for the class.

    For documentation about this data format:
    https://github.com/NVIDIA/DIGITS/blob/digits-5.0/docs/ImageFolderFormat.md
    """
    def __init__(self, source):
        self.loader = pencroft.open(source)
        classes = set()
        for key in self.loader.keys():
            classes.add(self._classname_from_key(key))
        self._classes = sorted(list(classes))

        # Used to convert string classnames to integer labels
        self._classname_to_label = dict([
            (classname, i) for i, classname in enumerate(self._classes)
        ])

    def __len__(self):
        return len(self.loader.keys())

    def num_classes(self):
        return len(self._classes)

    @staticmethod
    def _classname_from_key(key):
        return key.split(os.path.sep)[0]

    def generator(self):
        """
        Iterating yields an infinite number of (data, label) tuples, where data
        is a numpy array containing a barch of image data, and label is a numpy
        array containing a batch of label data."""

        # Each thread gets its own randomized set of keys
        keys = self.loader.keys()

        while True:
            random.shuffle(keys)
            data_batch = []
            label_batch = []

            for key in keys:
                data = self.loader.get(key)
                s = StringIO(data)
                img = PIL.Image.open(s)
                img = img.resize((224, 224))
                img = img.convert('RGB')
                data_batch.append(np.array(img))

                label_str = self._classname_from_key(key)
                label_int = self._classname_to_label[label_str]
                label_arr = np.zeros(self.num_classes())
                label_arr[label_int] = 1  # one-hot encoding
                label_batch.append(label_arr)

                if len(data_batch) == 32:  # batch size
                    yield np.array(data_batch), np.array(label_batch)
                    data_batch = []
                    label_batch = []
