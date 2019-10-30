from validation.dimvalidator import valid_dimensions
import validation.circle_detection.CircleDetection as cd
from PIL import Image


def validate(img):
    if not valid_dimensions(img):
        return False
    validated_image = cd.ValidatedImage(img)
    validated_image.circle_detection()
    if validated_image.is_valid:
        return True

