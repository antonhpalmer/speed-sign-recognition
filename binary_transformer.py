from validation.validator import validate as validate
from preprocessor.preproccesor import preprocess_image_test
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
    amt_opened = 0
    amt_validated = 0

    for directive in os.listdir(input_folder):
        for img in os.listdir(input_folder + directive):
            file_path = input_folder + directive + "/" + img
            image = Image.open(file_path)
            validated_image = validate(image)
            amt_opened += 1

            if validated_image.is_valid is True:
                amt_validated += 1

            if validated_image.is_valid is True:
                cropped_image = preprocess_image_test(file_path, validated_image.circle_center)
                if cropped_image is not None:
                    try:
                        cropped_image.save(output_folder + directive + "/" + str(img))
                        cropped += 1
                    except:
                        print("error")
                else:
                    not_cropped += 1
    return cropped, not_cropped, amt_opened, amt_validated


input_folder = "test_data/new_test_images_separated/"
output_folder = "test_data/disasterfolder/"

# Create directives if they do not exist with the same name in the output folder for the grayscaled images.
create_folders(input_folder, output_folder)

# Create a grayscaled image for every image in the folder training_images.
cropped_yes, cropped_no, amt_opened, amt_validated = create_grayscaled_for_folder(input_folder, output_folder)

# Removes wrongly cropped images
removed = remove_wrong_images(output_folder)

print("Cropped:", cropped_yes)
print("Not cropped:", cropped_no)
print("Removed:", removed)
print("Amount opened:", amt_opened)
print("amount validated:", amt_validated)
