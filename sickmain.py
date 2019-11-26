from validation.validator import validate as validate
from preprocessor.preproccesor import preprocess_image
import os
from PIL import Image

def remove_wrong_images(folder):
    removed = 0
    for directive in os.listdir(folder):
        for img in os.listdir(folder + directive):
            file_path = folder + directive + "/" + img
            if os.path.getsize(file_path) < 50:
                os.remove(file_path)
                removed += 1
    return removed


def create_folders(input_folder, output_folder):
    for directive in os.listdir(input_folder):
        if not os.path.exists(output_folder + directive):
            os.makedirs(output_folder + directive)
            print("created:", directive)

def create_grayscaled_for_folder(input_folder, output_folder):
    cropped = 0
    not_cropped = 0

    for directive in os.listdir(input_folder):
        for img in os.listdir(input_folder + directive):
            file_path = input_folder + directive + "/" + img
            image = Image.open(file_path)
            goodness, (x, y) = validate(image)
            if goodness is True:
                cropped_image = preprocess_image(file_path, (x, y))
                if cropped_image is not None:
                    try:
                        cropped_image.save(output_folder + directive + "/" + str(img))
                        cropped += 1
                    except:
                        print("error")
                else:
                    not_cropped += 1
    return cropped, not_cropped


training_images_path = "C:/Users/frede/PycharmProjects/speed-sign-recognition/test_data/new_test_images_separated/"
training_images_gray_path = "C:/Users/frede/PycharmProjects/speed-sign-recognition/test_data/new_test_images_separated_binary/"
removed = 0

# Create directives if they do not exist with the same name in the output folder for the grayscaled images.
create_folders(training_images_path, training_images_gray_path)

# Create a grayscaled image for every image in the folder training_images.
cropped_a, not_cropped_a = create_grayscaled_for_folder(training_images_path, training_images_gray_path)

# Removes wrongly cropped images
removed_a = remove_wrong_images(training_images_gray_path)

print("Cropped:", cropped_a)
print("Not cropped:", not_cropped_a)
print("Removed:", removed_a)