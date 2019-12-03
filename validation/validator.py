from validation.dim_validator import valid_dimensions
import validation.circle_detection.CircleDetection as cd


def validate(img):
    if not valid_dimensions(img):
        return False, (None, None)
    validated_image = cd.ValidatedImage(img)
    validated_image.circle_detection()
    return validated_image




