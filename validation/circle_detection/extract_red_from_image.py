from PIL import Image
from preprocessor.color_recognizor import red_validator

import os


def filter_red(input_img):
    img = input_img.copy()
    img_loaded = img.load()

    (width, height) = img.size

    for i in range(width):
        for j in range(height):
            (r, g, b) = img_loaded[i, j]

            if red_validator(r, g, b) is False:
                img_loaded[i, j] = (0, 0, 0)

    return img



# def make_filtered_images_with_circles(input_folder):
#
#     for directive in os.listdir(input_folder):
#         for img in os.listdir(input_folder + directive):
#             file_path_plus_name = input_folder + directive + '/' + img
#             filtered_image = filter_red(file_path_plus_name)
#
#             validator_object = CircleDetection.ValidatedImage(filtered_image)
#             validator_object.circle_detection()
#             validator_object.draw_circle('/home/simkortet/PycharmProjects/speed-sign-recognition/validation'
#                                          '/circle_detection/red_filtered_with_circle/' + directive + '/', img)

# make_filtered_images_with_circles('/home/simkortet/PycharmProjects/speed-sign-recognition/test_data/test_images/')
