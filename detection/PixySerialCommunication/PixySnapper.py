#  Copyright (c) 2019.
#  AAU, Student project group sw504e19, 2019.
#  Use this as reference to coding conventions in Python: https://github.com/kengz/python

from PIL import Image
import subprocess
from pathlib import Path


def snap_image():
    subprocess.call(['./PixySerialCommunication/get_raw_frame'])
    return Path("out.ppm")


def crop_image(path, x1, y1, x2, y2):
    Image.open(path).crop((x1, y1, x2, y2)).save("cropped.ppm")
    return Path("cropped.ppm")


def get_cropped_image(x, y, width, height):
    topleft_x = x - (width / 2)
    topleft_y = y - (height / 2)
    input_image = snap_image()
    cropped_image = crop_image(input_image, topleft_x, topleft_y, topleft_x + width, topleft_y + height)
    return cropped_image
