from validation.dim_validator import valid_dimensions


def validate(img):
    if valid_dimensions(img):
        return True
    return False
