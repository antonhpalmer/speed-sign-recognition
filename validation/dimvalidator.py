from PIL import Image


def valid_dimensions(image):
    width, height = image.size
    if max(width, height) / min(width, height) > 3:
        return False
    else:
        return True;
