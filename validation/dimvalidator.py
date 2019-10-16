def valid_dimensions(image):
    width, height = image.size
    if max(width, height) / min(width, height) > 2:
        return False
    else:
        return True
