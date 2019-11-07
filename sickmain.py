from validation.validator import validate as validate
from boxfinder import crop_image
import os
from PIL import Image

path = "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images/8/"
for elem in os.listdir(path):
    if "1.0" in str(elem):
        complete_path = path + elem
        image = Image.open(path + elem)
        goodness, (x, y) = validate(image)

        if goodness is True:
            crop_image(path + elem, (x, y), str(elem))
