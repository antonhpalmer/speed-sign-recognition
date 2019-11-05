#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import numpy as np
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
from keras.optimizers import SGD
from keras_preprocessing.image import ImageDataGenerator

from classification.models import models
from classification import definitions, preprocessing
from classification.definitions import IMG_SIZE, BATCH_SIZE

class ModelTrainer:
    def __init__(self, images_dir_path, learning_rate):
        self.images_dir_path = images_dir_path
        self.learning_rate = learning_rate

    def __lr_schedule(self, epoch):
        return self.learning_rate * (0.1 ** int(epoch / 10))

    def train_model(self, model, new_model_path, epochs):
        imgs = []
        labels = []
        preprocessing.preprocess_all_images(self.images_dir_path, imgs, labels)
        self.train_model(imgs, labels, model, new_model_path, epochs)

    def train_model(self, imgs, labels, model, new_model_path, epochs):
        X = np.array(imgs, dtype='float32')
        Y = np.eye(definitions.NUM_CLASSES, dtype='uint8')[labels]

        # train the model using SGD + momentum
        sgd = SGD(lr=self.learning_rate, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])

        model.fit(X, Y,
                  batch_size=definitions.BATCH_SIZE,
                  epochs=epochs,
                  validation_split=0.2,
                  callbacks=[LearningRateScheduler(self.__lr_schedule),
                             ModelCheckpoint(new_model_path, save_best_only=False)]
                  )

    # create a data generator
    def train(self, model):
        data_generator = ImageDataGenerator()
        training_iterator = data_generator.flow_from_directory(self.images_dir_path,
                                                               class_mode='categorical',
                                                               batch_size=BATCH_SIZE,
                                                               target_size=(IMG_SIZE, IMG_SIZE))

        new_model_path = 'test_data/new_model.h5'
        number_of_training_imgs = 21096
        steps_per_epoch = number_of_training_imgs / BATCH_SIZE

        sgd = SGD(lr=self.learning_rate, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])
        model.fit_generator(training_iterator, steps_per_epoch=steps_per_epoch, epochs=10,
                            callbacks=[LearningRateScheduler(self.__lr_schedule),
                                       ModelCheckpoint(new_model_path, save_best_only=False)]
                            )

