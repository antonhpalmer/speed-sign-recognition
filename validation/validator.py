from validation.dimvalidator import valid_dimensions


def validate(img):
    if valid_dimensions(img) == True:
        return True
