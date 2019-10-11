#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import glob
import os

import numpy as np
from skimage import color, exposure, transform
from skimage import io

from classification import definitions
from classification.training.training import ModelTrainer


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
    img = transform.resize(img, (definitions.IMG_SIZE, definitions.IMG_SIZE))

    # roll color axis to axis 0
    img = np.rollaxis(img, -1)

    return img


def preprocess_all_images(images_dir_path, imgs, labels):
    all_img_paths = glob.glob(os.path.join(images_dir_path, '*/*.ppm'))
    np.random.shuffle(all_img_paths)
    number_of_images = len(all_img_paths)
    count = 1
    for img_path in all_img_paths:
        img_path = img_path.replace("\\", "/")
        if count % 1000 == 0 or count == number_of_images:
            print(str(count) + "/" + str(number_of_images))
        img = preprocess_img(io.imread(img_path))
        label = ModelTrainer.get_class(img_path)
        imgs.append(img)
        labels.append(label)
        count += 1
