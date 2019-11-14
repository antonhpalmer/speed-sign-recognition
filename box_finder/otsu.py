import cv2
from PIL import Image


def apply_otsu_algorithm(image):
    img = cv2.imread(image, 0)
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(th2)
