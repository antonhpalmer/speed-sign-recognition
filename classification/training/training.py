#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import numpy as np
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
from keras.optimizers import SGD

from classification import definitions, preprocessing


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

        model.fit_generator()

        model.fit(X, Y,
                  batch_size=definitions.BATCH_SIZE,
                  epochs=epochs,
                  validation_split=0.2,
                  callbacks=[LearningRateScheduler(self.__lr_schedule),
                             ModelCheckpoint(new_model_path, save_best_only=False)]
                  )
