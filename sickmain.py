from validation.validator import validate as validate
from test import crop_image
import os
from PIL import Image

path = "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images/8/"
cropped = 0
not_cropped = 0
for elem in os.listdir(path):
    if "1.0" in str(elem):
        complete_path = path + elem
        image = Image.open(path + elem)
        goodness, (x, y) = validate(image)
        if goodness is True:
            a,b = crop_image(path + elem, (x, y), str(elem))
            cropped += a
            not_cropped += b
print("Cropped:", cropped)
print("Not cropped:", not_cropped)
