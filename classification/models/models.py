#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

from keras import backend as K
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.pooling import MaxPooling2D
from keras.models import Sequential

from classification import definitions

K.set_image_data_format('channels_first')


def get_cnn_model():
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=(3, definitions.IMG_SIZE, definitions.IMG_SIZE),
                     activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), padding='same',
                     activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(128, (3, 3), padding='same',
                     activation='relu'))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(definitions.NUM_CLASSES, activation='softmax'))
    return model


def get_model1():
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=(3, definitions.IMG_SIZE, definitions.IMG_SIZE),
                     activation='relu'))
    model.add(Dense(definitions.NUM_CLASSES, activation='softmax'))
    return model
