import re
from test_data.image_transformer.path_exception import PathException

from PIL import Image
from PIL import ImageEnhance


def create_output_image_path(path_to_image_before, appended_name):
    info = re.search('(.+?).ppm', path_to_image_before)
    if info:
        return str(info.group(1) + appended_name + ".ppm")
    else:
        raise PathException('The given path:', path_to_image_before, ", did not end on .ppm")


def transform_brightness(path_to_image):
    image_before = Image.open(path_to_image)
    brightness_enhancer = ImageEnhance.Brightness(image_before)

    brightness_list = [0.3, 0.5, 1.5, 2.0, 2.3]

    for brightness in brightness_list:
        appended_name = "(b=" + str(brightness) + ")"
        path_to_output_image = create_output_image_path(path_to_image, appended_name)
        brightness_enhancer.enhance(brightness).save(path_to_output_image)


transform_brightness("test_images/1.ppm")

