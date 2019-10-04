import os
import numpy as np
from keras.preprocessing import image
from skimage import io
from keras.models import load_model

import pandas as pd
from skimage import color, exposure, transform

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
test = pd.read_csv('GTSRB/GT-final_test.csv', sep=';')

# Load test dataset
X_test = []
y_test = []
i = 0
for file_name, class_id in zip(list(test['Filename']), list(test['ClassId'])):
    img_path = os.path.join('GTSRB/Final_Test/Images/', file_name)
    X_test.append(preprocess_img(io.imread(img_path)))
    y_test.append(class_id)

X_test = np.array(X_test)
y_test = np.array(y_test)
'''
model = load_model('model.h5')
'''
# predict and evaluate
y_pred = model.predict_classes(X_test)
acc = np.sum(y_pred == y_test) / np.size(y_pred)
print("Test accuracy = {}".format(acc))
'''
testImage = image.load_img('00001.ppm', target_size=(IMG_SIZE, IMG_SIZE))
testImage = image.img_to_array(testImage)
testImage = np.expand_dims(testImage, axis=0)
result = model.predict(testImage)
print(result)
'''
test_image = image.load_img('frog.jpg', target_size=(32, 32))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = loaded_model.predict(test_image)

# np.set_printoptions(formatter={'float_kind':'{:f}'.format})
print(result)
'''
