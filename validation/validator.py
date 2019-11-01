from validation.dim_validator import valid_dimensions
import validation.circle_detection.CircleDetection as cd
from PIL import Image


def validate(img, counter):
    if not valid_dimensions(img):
        return False
    validated_image = cd.ValidatedImage(img)
    validated_image.circle_detection()
    if validated_image.is_valid:
        validated_image.draw_circle('C:/Users/sujee/PycharmProjects/speed-sign-recognition/validation/img/validated_images/', str(counter) + '.ppm')
        #return True, validated_image.circle_center
        return True, validated_image.circle_center
    else:
        return False, (None, None)




