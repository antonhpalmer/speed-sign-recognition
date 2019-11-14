from validation.validator import validate as validate
from test import crop_image
import os
from PIL import Image

input_path = "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images/"
output_path = "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images_gray/"

cropped = 0
not_cropped = 0
removed = 0

# Create directives if they do not exist with the same name in the output folder for the grayscaled images.
for directive in os.listdir(input_path):
    if not os.path.exists(output_path + directive):
        os.makedirs(output_path + directive)
        print("created:", directive)

# Create a grayscaled image for every image in the folder training_images.
for directive in os.listdir(input_path):
    for img in os.listdir(input_path + directive):
        file_path = input_path + directive + "/" + img
        image = Image.open(file_path)
        goodness, (x, y) = validate(image)
        if goodness is True:
            cropped_image = crop_image(file_path, (x, y))
            if cropped_image is not None:
                try:
                    cropped_image.save(output_path + directive + "/" + str(img))
                    cropped += 1
                except:
                    print("error")
            else:
                not_cropped += 1

# Removes wrongly cropped images
for directive in os.listdir(output_path):
    for img in os.listdir(output_path + directive):
        file_path = output_path + directive + "/" + img
        if os.path.getsize(file_path) < 50:
            os.remove(file_path)
            removed +=1

print("Cropped:", cropped)
print("Not cropped:", not_cropped)
print("Removed:", removed)