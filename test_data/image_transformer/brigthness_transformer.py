from path_transformer.output_path_creator import create_output_path
from PIL import Image
from PIL import ImageEnhance
import os


def create_output_folder(folder_path):
    output_folder_path = folder_path + "transformed/"
    if os.path.exists(output_folder_path):
        return output_folder_path
    else:
        try:
            os.mkdir(output_folder_path)
        except OSError:
            print("Creation of the directory %s failed" % output_folder_path)
        return output_folder_path


def create_new_file_name(file_name, appended_name, file_type):
    temp = file_name.rstrip(file_type)  # We remove the file type from the file name
    return temp + appended_name + file_type


def create_image_output_path(image_name, output_folder_path, appended_name):
    image_type = ".ppm"
    new_file_name = create_new_file_name(image_name, appended_name, image_type)
    return output_folder_path + new_file_name


def transform_brightness(image_name, folder_path):
    path_to_image = folder_path + image_name
    image_before = Image.open(path_to_image)
    brightness_enhancer = ImageEnhance.Brightness(image_before)

    brightness_list = [0.3, 0.5, 1.0, 1.5, 2.0, 2.3]

    output_folder_path = create_output_folder(folder_path)

    output_path_list = []
    for brightness in brightness_list:
        appended_name = "(b=" + str(brightness) + ")"
        path_to_output_image = create_image_output_path(image_name, output_folder_path, appended_name)
        output_path_list.append(path_to_output_image)
        brightness_enhancer.enhance(brightness).save(path_to_output_image)

    return output_path_list





