'''
PREPROCESSING FUNCTION DEFINITION
'''
import numpy as np
from skimage import color, exposure, transform

from Models.cnn_model import cnn_model
from Models.model1 import model1

NUM_CLASSES = 8
IMG_SIZE = 48

def preprocess_img(img):
    # Histogram normalization in v channel
    hsv = color.rgb2hsv(img)
    hsv[:, :, 2] = exposure.equalize_hist(hsv[:, :, 2])
    img = color.hsv2rgb(hsv)

    # central square crop
    min_side = min(img.shape[:-1])
    centre = img.shape[0] // 2, img.shape[1] // 2
    img = img[centre[0] - min_side // 2:centre[0] + min_side // 2,
          centre[1] - min_side // 2:centre[1] + min_side // 2,
          :]

    # rescale to standard size
    img = transform.resize(img, (IMG_SIZE, IMG_SIZE))

    # roll color axis to axis 0
    img = np.rollaxis(img, -1)

    return img


'''
PREPROCESSING ALL IMAGES
'''
from skimage import io
import os
import glob

def get_class(img_path):
    return int(img_path.split('/')[-2])

root_dir = 'GTSRB/Final_Training/Images/'
imgs = []
labels = []

all_img_paths = glob.glob(os.path.join(root_dir, '*/*.ppm'))
np.random.shuffle(all_img_paths)
count = 1
number_of_images = len(all_img_paths)
for img_path in all_img_paths:
    img_path = img_path.replace("\\", "/")
    if count % 1000 == 0 or count == number_of_images:
        print(str(count) + "/" + str(number_of_images))

    count += 1

    img = preprocess_img(io.imread(img_path))
    label = get_class(img_path)
    imgs.append(img)
    labels.append(label)

X = np.array(imgs, dtype='float32')
# Make one hot targets
Y = np.eye(NUM_CLASSES, dtype='uint8')[labels]




'''
LOSS-FUNCTION, OPTIMIZER & METRIC SPECIFICATION
'''
from keras.optimizers import SGD

model = model1()
# let's train the model using SGD + momentum
lr = 0.01
sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])



'''
THE ACTUAL TRAINING
'''
from keras.callbacks import LearningRateScheduler, ModelCheckpoint

def lr_schedule(epoch):
    return lr * (0.1 ** int(epoch / 10))

batch_size = 32
epochs = 5
model.fit(X, Y,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.2,
          callbacks=[LearningRateScheduler(lr_schedule),
                     ModelCheckpoint('model1.h5', save_best_only=True)]
          )
