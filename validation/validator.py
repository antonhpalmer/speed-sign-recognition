from validation.dimvalidator import valid_dimensions


def validate(img):
    if valid_dimensions(img):
        return True
    return False
