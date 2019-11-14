#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python
import os

import numpy as np
import matplotlib.pyplot as plt
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

    def train(self, model, train_dir, val_dir, epochs):
        training_datagen = ImageDataGenerator(
            rotation_range=15,
            zoom_range=0.15,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.15,
            horizontal_flip=False,
            fill_mode="nearest"
        )
        val_datagen = ImageDataGenerator()
        training_iterator = training_datagen.flow_from_directory(train_dir,
                                                                 class_mode='categorical',
                                                                 batch_size=BATCH_SIZE,
                                                                 target_size=(IMG_SIZE, IMG_SIZE)
                                                                 )

        val_iterator = val_datagen.flow_from_directory(val_dir,
                                                       class_mode='categorical',
                                                       batch_size=BATCH_SIZE,
                                                       target_size=(IMG_SIZE, IMG_SIZE)
                                                       )

        # TODO: Remove ModelCheckPoint as we dont want to save the model
        new_model_path = 'test_data/new_model.h5'
        history = model.fit_generator(training_iterator, epochs=epochs, shuffle=True,
                                      callbacks=[ModelCheckpoint(new_model_path, save_best_only=True)],
                                      validation_data=val_iterator
                                      )

        return history

    def plot_acc_and_loss(self, history, accuracy_plot_path, loss_plot_path):
        print(history.history.keys())
        # Plot training & validation accuracy values
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper left')
        plt.savefig(accuracy_plot_path, bbox_inches='tight')
        plt.clf()

        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper left')
        plt.savefig(loss_plot_path, bbox_inches='tight')
        plt.clf()
