#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python
import os

import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks import LearningRateScheduler, ModelCheckpoint, EarlyStopping
from keras.optimizers import SGD
from keras_preprocessing.image import ImageDataGenerator

from classification.models import models
from classification import definitions, preprocessing
from classification.definitions import IMG_SIZE, BATCH_SIZE


class ModelTrainer:
    def __init__(self, compiled_model):
        self.compiled_model = compiled_model

    def train(self, train_dir, val_dir, model_save_path, epochs, color_mode):
        training_datagen = ImageDataGenerator(
            rotation_range=15,
            zoom_range=0.15,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.15,
            horizontal_flip=False,
            fill_mode="nearest"
        )
        training_iterator = training_datagen.flow_from_directory(train_dir,
                                                                 class_mode='categorical',
                                                                 batch_size=BATCH_SIZE,
                                                                 target_size=(IMG_SIZE, IMG_SIZE),
                                                                 color_mode=color_mode
                                                                 )

        val_datagen = ImageDataGenerator()
        val_iterator = val_datagen.flow_from_directory(val_dir,
                                                       class_mode='categorical',
                                                       batch_size=BATCH_SIZE,
                                                       target_size=(IMG_SIZE, IMG_SIZE),
                                                       color_mode=color_mode
                                                       )

        history = self.compiled_model.fit_generator(training_iterator, epochs=epochs, shuffle=True,
                                                    validation_data=val_iterator,
                                                    callbacks=[ModelCheckpoint(model_save_path, save_best_only=True,
                                                                               monitor='val_accuracy', verbose=1),
                                                               EarlyStopping(monitor='val_accuracy', patience=20, verbose=1)])
        return history

    def plot_acc_and_loss(self, history, accuracy_plot_path, loss_plot_path):
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

    def write_model_summary_to_file(self, file):
        return self.compiled_model.summary(print_fn=lambda x: file.write(x + '\n'))

