from path_transformer.output_path_creator import create_output_path
from PIL import Image
from PIL import ImageEnhance


def transform_brightness(path_to_image):
    image_before = Image.open(path_to_image)
    brightness_enhancer = ImageEnhance.Brightness(image_before)

    brightness_list = [0.3, 0.5, 1.5, 2.0, 2.3]

    for brightness in brightness_list:
        appended_name = "(b=" + str(brightness) + ")"
        path_to_output_image = create_output_path(path_to_image, ".ppm", appended_name)
        brightness_enhancer.enhance(brightness).save(path_to_output_image)


transform_brightness("test_images/1.ppm")

