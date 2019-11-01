import validation.validator as validator
from PIL import Image
import os
import os


validated_counter = 0
rejected_counter = 0
"""for i in range (0, 700):

    if os.path.exists("C:/Users/sujee/Desktop/P5/Images/" + str(i) + ".ppm"):
        #img = Image.open("C:/Users/sujee/PycharmProjects/speed-sign-recognition/testdata/Images/" + str(i) + ".ppm")
        img = Image.open("C:/Users/sujee/Desktop/P5/Images/" + str(i) + ".ppm")

        if validator.validate(img):
            validated_counter += 1
        else:
            # img.save("rejected_images/" + str(i) + ".jpg")
            rejected_counter += 1

print("Number of validated: " + str(validated_counter))
print("Number of rejected: " + str(rejected_counter))
"""
path = 'C:/Users/sujee/PycharmProjects/speed-sign-recognition/test_data/training_images/'
print(len(os.listdir(path)))
for file in os.listdir(path):
    image = Image.open(path + file)

    validation_status, (a, b) = validator.validate(image, validated_counter)

    if validation_status:
        validated_counter += 1
    else:
        rejected_counter += 1

print("Number of validated: " + str(validated_counter))
print("Number of rejected: " + str(rejected_counter))