#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

import subprocess

from PIL import Image

EXTRA_PIXELS = 15


def snap_image():
    subprocess.call(['./detection/pixy_serial_communication/get_raw_frame'])
    return Image.open("out.ppm")


def crop_image(img, x1, y1, x2, y2):
    img.crop((x1, y1, x2, y2)).save("cropped.ppm")
    return Image.open("cropped.ppm")


def crop_image_test(img, x1, y1, x2, y2):
    img.crop((x1, y1, x2, y2)).save("croppedDefault.ppm")
    return Image.open("cropped.ppm")


def get_cropped_image(x, y, width, height):
    topleft_x = x - (width / 2) - EXTRA_PIXELS
    topleft_y = y - (height / 2) - EXTRA_PIXELS
    bottomright_x = x + (width / 2) + EXTRA_PIXELS
    bottomright_y = y + (height / 2) + EXTRA_PIXELS

    input_image = snap_image()
    width, height = input_image.size

    if topleft_y < 1:
        topleft_y = 1
    if topleft_x < 1:
        topleft_x = 1
    if bottomright_x > width:
        bottomright_x = width
    if bottomright_y > height:
        bottomright_y = height

    cropped_image = crop_image(input_image, topleft_x, topleft_y, bottomright_x, bottomright_y)
    return cropped_image
