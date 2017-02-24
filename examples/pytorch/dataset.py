from cStringIO import StringIO
import os

import numpy as np
import PIL.Image
import torch.utils.data

import pencroft


class PencroftDataset(torch.utils.data.Dataset):
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

    def num_classes(self):
        return len(self._classes)

    @staticmethod
    def _classname_from_key(key):
        return key.split(os.path.sep)[0]

    def __len__(self):
        return len(self.loader)

    def __getitem__(self, index):
        key, data = self.loader[index]

        # convert data
        s = StringIO(data)
        img = PIL.Image.open(s)
        img = img.resize((224, 224))
        img = img.convert('RGB')
        data = np.array(img)
        data = data.transpose(2, 0, 1)  # to CHW

        label_str = self._classname_from_key(key)
        label_int = self._classname_to_label[label_str]

        return (
            torch.from_numpy(data.astype('float32')),
            label_int,
        )
