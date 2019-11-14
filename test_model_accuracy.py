import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import load_model
from skimage import io
from classification import preprocessing, definitions
from classification.models import models
from classification.test.test import ModelTester
from classification.training.training import ModelTrainer
from keras.preprocessing import image
import numpy as np
from keras.optimizers import SGD
from keras_preprocessing.image import ImageDataGenerator

class TestModelAccuracy:
    def create_systematic_test(self, all_models_dir, train_dir, val_dir, test_dir):
        i = 0
        for optimizer in ('sgd', 'adam', 'RMSprop', 'Adamax'):
            for num_conv_layers in range(1, 9):
                for num_pooling_layers in range(0, num_conv_layers):
                    for num_dropout_layers in range(0, num_conv_layers):
                        i += 1


                        #models.get_conv2d_layer()
        print(i)










    all_models_dir = 'classification/systematic_model_test/'
    train_dir_path = 'test_data/training_images/'
    val_dir_path = 'test_data/val_images/'
    test_dir_path = 'test_data/test_images/'

    create_systematic_test(None, all_models_dir, train_dir_path, val_dir_path, test_dir_path)






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