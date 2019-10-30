from path_transformer.output_path_creator import create_output_path
from PIL import Image
from PIL import ImageEnhance


def transform_brightness(image_name, folder_path):
    path_to_image = folder_path + image_name
    image_before = Image.open(path_to_image)
    brightness_enhancer = ImageEnhance.Brightness(image_before)

    brightness_list = [0.3, 0.5, 1.0, 1.5, 2.0, 2.3]

    output_path_list = []
    for brightness in brightness_list:
        appended_name = "(b=" + str(brightness) + ")"
        path_to_output_image = create_output_path(path_to_image, ".ppm", appended_name)
        output_path_list.append(path_to_output_image)
        brightness_enhancer.enhance(brightness).save(path_to_output_image)

    return output_path_list





