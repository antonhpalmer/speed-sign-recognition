from validation.validator import validate as validate
from boxfinder import crop_image
import os
from PIL import Image

path = "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images/30/"
i = 0
for elem in os.listdir(path):
    complete_path = path + elem
    image = Image.open(path + elem)
    goodness, (x,y) = validate(image)

    if goodness is True:
        print(x,y)
        crop_image(path + elem, (x,y), str(elem))
        i += 1
