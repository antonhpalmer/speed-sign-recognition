from validation.circle_detection.extract_red_from_image import filter_red
from validation.dim_validator import valid_dimensions
import validation.circle_detection.CircleDetection as cd


def validate(img):
    if not valid_dimensions(img):
        validated_image = cd.ValidatedImage(img)
        validated_image.is_valid = False
        return validated_image
    red_img = filter_red(img)
    validated_image = cd.ValidatedImage(red_img)
    validated_image.circle_detection()
    validated_image.img = img
    return validated_image




