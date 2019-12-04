from validation.dim_validator import valid_dimensions
import validation.circle_detection.CircleDetection as cd


def validate(img):
    if not valid_dimensions(img):
        validated_image = cd.ValidatedImage(img)
        validated_image.is_valid = False
        return validated_image
    validated_image = cd.ValidatedImage(img)
    validated_image.circle_detection()
    return validated_image




