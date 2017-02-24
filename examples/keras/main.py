#!/usr/bin/env python

import argparse
import time

import keras
import keras.applications
import keras.preprocessing.image

from loader import Loader


def train(source, use_keras_loader=False, nb_worker=1, pickle_safe=False,
          use_resnet50=False):
    start_time = time.time()

    if use_keras_loader:
        preprocessor = keras.preprocessing.image.ImageDataGenerator()
        generator = preprocessor.flow_from_directory(
            source,
            target_size=(224, 224),
            color_mode='rgb',
        )
        count = generator.nb_sample
        num_classes = generator.nb_class
    else:
        loader = Loader(source)
        if nb_worker > 1:
            if pickle_safe:
                loader.loader.make_mp_safe()
            else:
                loader.loader.make_thread_safe()
        generator = loader.generator()
        count = len(loader)
        num_classes = loader.num_classes()

    if use_resnet50:
        pretrained_model = keras.applications.resnet50.ResNet50(
            input_shape=(224, 224, 3),
            include_top=False)
        x = pretrained_model.output
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(num_classes)(x)
        model = keras.models.Model(input=pretrained_model.input,
                                   output=x)
    else:
        model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=(224, 224, 3)),
            keras.layers.Dense(num_classes),
        ])

    model.compile(
        loss='categorical_crossentropy',
        optimizer='sgd',
        metrics=['accuracy'],
    )

    model.fit_generator(
        generator, count, 1,
        nb_worker=nb_worker,
        pickle_safe=pickle_safe,
    )
    print('Finished in %f seconds.' % (time.time() - start_time,))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Train ResNet50 on one epoch of DATA')
    parser.add_argument('source')
    parser.add_argument('--keras_loader', action='store_true')
    parser.add_argument('--nb_worker', type=int, default=1)
    parser.add_argument('--pickle_safe', action='store_true')
    parser.add_argument('--use_resnet50', action='store_true')
    args = parser.parse_args()
    train(
        args.source,
        use_keras_loader=args.keras_loader,
        nb_worker=args.nb_worker,
        pickle_safe=args.pickle_safe,
        use_resnet50=args.use_resnet50,
    )
