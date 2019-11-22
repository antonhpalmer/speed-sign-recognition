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
from keras.optimizers import SGD, RMSprop, Adamax, Adam
from keras_preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.pooling import MaxPooling2D
from classification.definitions import IMG_SIZE, BATCH_SIZE, NUM_CLASSES

class TestModelAccuracy:
    def add_conv_and_pooling(self, model, filters, kernel_size, add_input_shape, color_channels):
        if add_input_shape:
            model.add(Conv2D(filters, kernel_size=kernel_size,
                             padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, color_channels)))
        else:
            model.add(Conv2D(filters, kernel_size=kernel_size,
                             padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))

    def add_conv_and_pooling_w_dropout(self, model, filters, kernel_size, dropout_rate, add_input_shape, color_channels):
        self.add_conv_and_pooling(model, filters, kernel_size, add_input_shape, color_channels)
        model.add(Dropout(dropout_rate))

    def add_two_conv_and_pooling(self, model, filters, kernel_size, add_input_shape, color_channels):
        if add_input_shape:
            model.add(Conv2D(filters, kernel_size=kernel_size,
                             padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, color_channels)))
        else:
            model.add(Conv2D(filters, kernel_size=kernel_size, padding='same', activation='relu'))
        model.add(Conv2D(filters, kernel_size=kernel_size, padding='same', activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_last'))

    def add_two_conv_and_pooling_w_dropout(self, model, filters, kernel_size, dropout_rate, add_input_shape, color_channels):
        self.add_two_conv_and_pooling(model, filters, kernel_size, add_input_shape, color_channels)
        model.add(Dropout(dropout_rate))

    def add_last_layers(self, model):
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(definitions.NUM_CLASSES, activation='softmax'))

    def train_all_models(self, all_models_dir, compiled_models, train_dir, val_dir, color_mode):
        for model in compiled_models:
            print('NOW TRAINING: ' + model.name)
            model_dir_path = os.path.join(all_models_dir, model.name)
            os.makedirs(model_dir_path, exist_ok=True)
            acc_plot_path = os.path.join(model_dir_path, model.name + '_acc.png')
            loss_plot_path = os.path.join(model_dir_path, model.name + '_loss.png')
            summary_file_path = os.path.join(model_dir_path, model.name + '_info.txt')
            model_save_path = os.path.join(model_dir_path, model.name + '.h5')

            trainer = ModelTrainer(model)
            history = trainer.train(train_dir, val_dir, model_save_path, 500, color_mode)

            trainer.plot_acc_and_loss(history, acc_plot_path, loss_plot_path)

            with open(summary_file_path, mode='w', newline='') as summary_file:
                trainer.write_model_summary_to_file(summary_file)

    def create_systematic_architecture_test(self, all_models_dir, train_dir, val_dir, color_mode):
        if color_mode == 'grayscale':
            color_channels = 1
        else:
            color_channels = 3

        models = []
        param_str = '_opt=adam_ker=3_drop=20'

        # model = Sequential()
        # for i in (32, 64, 128, 256):
        #     model = Sequential(model.layers, name='model_singleconv_' + str(i) + param_str)
        #     self.add_conv_and_pooling(model, i, 3, i == 32, color_channels)
        #     models.append(model)
        #
        # model = Sequential()
        # for i in (32, 64, 128, 256):
        #     model = Sequential(model.layers, name='model_singleconv_wdropout_' + str(i) + param_str)
        #     self.add_conv_and_pooling_w_dropout(model, i, 3, 0.2, i == 32, color_channels)
        #     models.append(model)
        #
        # model = Sequential()
        # for i in (32, 64, 128, 256):
        #     model = Sequential(model.layers, name='model_doubleconv_' + str(i) + param_str)
        #     self.add_two_conv_and_pooling_w_dropout(model, i, 3, 0.2, i == 32, color_channels)
        #     models.append(model)

        model = Sequential()
        for i in (32, 64, 128, 256):
            model = Sequential(model.layers, name='model_doubleconv_nodrop_' + str(i) + param_str)
            self.add_two_conv_and_pooling(model, i, 3, i == 32, color_channels)
            models.append(model)

        for model in models:
            self.add_last_layers(model)
            model.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])

        self.train_all_models(all_models_dir, models, train_dir, val_dir, color_mode)

    def evaluate_all_models_in_dir(self, models_path, test_images_dir_path, new_test_images_dir_path):
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
                evaluation_file.write('test_images_binary;' + str(test_images_eval[1]) + '\n')
                evaluation_file.write('new_test_images_separated_binary;' + str(new_test_images_eval[1]) + '\n')

    def create_systematic_parameter_test(self, all_models_dir, train_dir, val_dir, color_mode):
        if color_mode == 'grayscale':
            color_channels = 1
        else:
            color_channels = 3
        models = []
        optimizers = {'sgd': SGD(), 'rmsprop': RMSprop(), 'adamax': Adamax(), 'adam': Adam()}
        kernel_sizes = [3, 5, 7]
        dropout_rates = [0.1, 0.2, 0.3, 0.4, 0.5]

        for optimizer in optimizers.keys():
            for kernel_size in kernel_sizes:
                for dropout_rate in dropout_rates:
                    model = Sequential()
                    self.add_two_conv_and_pooling_w_dropout(model, 32, kernel_size, dropout_rate, True, color_channels)
                    self.add_two_conv_and_pooling_w_dropout(model, 64, kernel_size, dropout_rate, False, color_channels)
                    self.add_last_layers(model)
                    model.name = 'model_doubleconv64_opt=' + optimizer + '_ker=' + str(kernel_size) + '_drop=' \
                                 + str(dropout_rate * 100)
                    model.compile(optimizer=optimizers.get(optimizer),
                                  loss='categorical_crossentropy',
                                  metrics=['accuracy'])
                    models.append(model)

        # making sure it does not train existing models
        for model in models:
            if os.path.exists(os.path.join(all_models_dir, model.name)):
                models.remove(model)
        self.train_all_models(all_models_dir, models, train_dir, val_dir, color_mode)








all_models_dir = 'classification/systematic_model_test_earlystopping/'
os.makedirs(all_models_dir, exist_ok=True)
train_dir_path = 'test_data/training_images/'
val_dir_path = 'test_data/val_images/'
test = TestModelAccuracy()
test.create_systematic_architecture_test(all_models_dir, train_dir_path, val_dir_path, 'rgb')
# test.create_systematic_parameter_test(all_models_dir, train_dir_path, val_dir_path, 'grayscale')


test_images_dir_path = 'test_data/test_images/'
new_test_images_dir_path = 'test_data/new_test_images_separated/'
models_path = 'classification/systematic_model_test_earlystopping/'
test = TestModelAccuracy()
test.evaluate_all_models_in_dir(models_path, test_images_dir_path, new_test_images_dir_path)


all_models_dir = 'classification/systematic_test_binary_params/'
os.makedirs(all_models_dir, exist_ok=True)
train_dir_path = 'test_data/training_images_binary/'
val_dir_path = 'test_data/val_images_binary/'
test = TestModelAccuracy()
# test.create_systematic_architecture_test(all_models_dir, train_dir_path, val_dir_path, 'grayscale')
test.create_systematic_parameter_test(all_models_dir, train_dir_path, val_dir_path, 'grayscale')

test_images_dir_path = 'test_data/test_images_binary/'
new_test_images_dir_path = 'test_data/new_test_images_separated_binary/'
models_path = 'classification/systematic_test_binary_params/'
test = TestModelAccuracy()
test.evaluate_all_models_in_dir(models_path, test_images_dir_path, new_test_images_dir_path)




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
