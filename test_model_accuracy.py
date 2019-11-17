import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import load_model
from skimage import io
from classification import preprocessing, definitions
from classification.models import models
from classification.test.test import ModelTester
from keras.models import Sequential
from classification.training.training import ModelTrainer
from keras.preprocessing import image
import numpy as np
from keras.optimizers import SGD
from keras_preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.pooling import MaxPooling2D
from classification.definitions import IMG_SIZE, BATCH_SIZE, NUM_CLASSES

class TestModelAccuracy:
    def add_conv_and_pooling(self, model, filters, add_input_shape):
        if add_input_shape:
            model.add(Conv2D(filters, (3, 3), padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)))
        else:
            model.add(Conv2D(filters, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))

    def add_conv_and_pooling_w_dropout(self, model, filters, add_input_shape):
        self.add_conv_and_pooling(model, filters, add_input_shape)
        model.add(Dropout(0.2))

    def add_two_conv_and_pooling_w_dropout(self, model, filters, add_input_shape):
        if add_input_shape:
            model.add(Conv2D(filters, (3, 3), padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)))
        else:
            model.add(Conv2D(filters, (3, 3), padding='same', activation='relu'))
        model.add(Conv2D(filters, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))
        model.add(Dropout(0.2))

    def add_last_layers(self, model):
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(definitions.NUM_CLASSES, activation='softmax'))

    def create_systematic_test(self, all_models_dir, train_dir, val_dir):
        models = []
        param_str = '_act=relu_opt=adam_ker=3_pad=same_drop=20'

        # model = Sequential()
        # for i in (32, 64, 128, 256):
        #     model = Sequential(model.layers, name='model_singleconv_' + str(i) + param_str)
        #     self.add_conv_and_pooling(model, i, i == 32)
        #     models.append(model)
        #
        # model = Sequential()
        # for i in (32, 64, 128, 256):
        #     model = Sequential(model.layers, name='model_singleconv_wdropout_' + str(i) + param_str)
        #     self.add_conv_and_pooling_w_dropout(model, i, i == 32)
        #     models.append(model)

        model = Sequential()
        for i in (32, 64, 128, 256):
            model = Sequential(model.layers, name='model_doubleconv_' + str(i) + param_str)
            self.add_two_conv_and_pooling_w_dropout(model, i, i == 32)
            models.append(model)

        for model in models:
            self.add_last_layers(model)


        for model in models:
            print('NOW TRAINING: ' + model.name)
            model_dir_path = os.path.join(all_models_dir, model.name)
            os.makedirs(model_dir_path, exist_ok=True)
            acc_plot_path = os.path.join(model_dir_path, model.name + '_acc.png')
            loss_plot_path = os.path.join(model_dir_path, model.name + '_loss.png')
            summary_file_path = os.path.join(model_dir_path, model.name + '_info.txt')
            model_save_path = os.path.join(model_dir_path, model.name + '.h5')

            model.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
            trainer = ModelTrainer(model)
            history = trainer.train(train_dir, val_dir, model_save_path, 80)

            trainer.plot_acc_and_loss(history, acc_plot_path, loss_plot_path)

            with open(summary_file_path, mode='w', newline='') as summary_file:
                trainer.write_model_summary_to_file(summary_file)

    def evaluate_all_models_in_dir(self, models_path):
        test_images_dir_path = 'test_data/test_images/'
        new_test_images_dir_path = 'test_data/new_test_images_separated'
        models = []
        for root, dirs, files in os.walk(models_path):
            for file in files:
                if '.h5' in file:
                    models.append(load_model(os.path.join(root, file)))

        for model in models:
            tester = ModelTester(model)
            test_images_eval = tester.evaluate_model(test_images_dir_path)
            print(test_images_eval)
            new_test_images_eval = tester.evaluate_model(new_test_images_dir_path)
            print(new_test_images_eval)

            os.makedirs(os.path.join(models_path, model.name), exist_ok=True)
            evaluation_file_path = os.path.join(models_path, model.name, model.name + '_eval.csv')
            with open(evaluation_file_path, mode='w') as evaluation_file:
                evaluation_file.write('Evaluation_dataset;Accuracy\n')
                evaluation_file.write('test_images;' + str(test_images_eval[1]) + '\n')
                evaluation_file.write('new_test_images_separated;' + str(new_test_images_eval[1]) + '\n')










all_models_dir = 'classification/systematic_model_test_w_saved_models/'
os.makedirs(all_models_dir, exist_ok=True)
train_dir_path = 'test_data/training_images/'
val_dir_path = 'test_data/val_images/'
test = TestModelAccuracy()
test.create_systematic_test(all_models_dir, train_dir_path, val_dir_path)





#
# models_path = 'C:/Users/anton/Desktop/P5/'
# test = TestModelAccuracy()
# test.evaluate_all_models_in_dir(models_path)





    # trainer = ModelTrainer(train_dir_path, 0.01)
    # model = models.get_model2()
    # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])
    # trainer.train(model, train_dir_path, val_dir_path)

    # test_datagen = ImageDataGenerator()
    # test_iterator = test_datagen.flow_from_directory('test_data/test_images/',
    #                                                  class_mode='categorical',
    #                                                  target_size=(IMG_SIZE, IMG_SIZE)
    #                                                  )


    # model = load_model('C:/Users/anton/Desktop/P5/new_model.h5')
    # test_datagen = ImageDataGenerator()
    # iterator = test_datagen.flow_from_directory('test_data/new_test_images_separated',
    #                                             target_size=(definitions.IMG_SIZE, definitions.IMG_SIZE))
    # evaluation = model.evaluate(iterator)
    # print(evaluation)
    # tester = ModelTester(model)
    # with open('test_data/new_model_summary.txt', mode='w', newline='') as file:
    #     tester.write_model_summary_to_file(file)

    # datagen = ImageDataGenerator()
    # iterator = datagen.flow_from_directory('test_data/test_images', target_size=(IMG_SIZE, IMG_SIZE))
    #
    # loss = model.evaluate_generator(iterator)
    # print(loss)
    # tester = ModelTester(model)
    # result = tester.classify_single_image('test_data/test_images/30/grouproom_floor_light4.ppm')
    # print(result)
    # print(classes[0])
    # print(definitions.ID_TO_SIGN_SWITCHER.get(np.argmax(classes[0])))

    # model = load_model('C:/Users/anton/Desktop/P5/new_model.h5')
    # tester = ModelTester(model)
    # classes = tester.classify_single_image('test_data/new_test_images_separated/60/sofa41.ppm')
    # print(classes)
