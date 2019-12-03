from PIL import Image
from PIL import ImageEnhance
from preprocessor.color_recognizor import red_validator

from preprocessor.directions import Direction
from preprocessor.no_red_pixel_exception import NoRedPixelException
from preprocessor.otsu import apply_otsu_algorithm
from preprocessor.wrong_center_exception import WrongCenterException


def check_neighbour_pixels(pix, x, y, red_pixels):
    neighbours = []

    if red_pixels is None:
        red_pixels = []

    if len(red_pixels) >= 10:
        return red_pixels

    neighbours.append((x + 1, y))
    neighbours.append((x - 1, y))
    neighbours.append((x, y + 1))
    neighbours.append((x, y - 1))


    for neighbour in neighbours:
        try:
            (x, y) = neighbour
            (r, g, b) = pix[x, y]
            if red_validator(r, g, b) is True and (x, y) not in red_pixels:
                red_pixels.append((x, y))
                red_pixels = check_neighbour_pixels(pix, x, y, red_pixels)
        except IndexError:
            print("pixel out of bounds")

    return red_pixels

def detect_red_cluster(pix, x, y):
    red_pixel_list = []

    (r, g, b) = pix[x, y]
    if red_validator(r, g, b) is True:
        red_pixel_list.append((x, y))
        return len(check_neighbour_pixels(pix, x, y, red_pixel_list))


def get_next_pixel_coordinate(x, y, direction):
    if direction == Direction.LEFT:
        return x - 1, y
    elif direction == Direction.RIGHT:
        return x + 1, y
    elif direction == Direction.UP:
        return x, y - 1
    elif direction == Direction.DOWN:
        return x, y + 1





def find_red_pixel(pix, x, y, direction):
    while True:
        try:
            size_of_cluster = detect_red_cluster(pix, x, y)
            if size_of_cluster > 10:
                return x, y
            x, y = get_next_pixel_coordinate(x, y, direction)
        except IndexError:
            raise NoRedPixelException("No red pixel found in the direction: " + direction)


def red_edge_detection(pix, x, y):
    left_pixel_x, left_pixel_y = find_red_pixel(pix, x, y, Direction.LEFT)
    right_pixel_x, right_pixel_y = find_red_pixel(pix, x, y, Direction.RIGHT)
    up_pixel_x, up_pixel_y = find_red_pixel(pix, x, y, Direction.UP)
    down_pixel_x, down_pixel_y = find_red_pixel(pix, x, y, Direction.DOWN)

    return left_pixel_x, right_pixel_x, up_pixel_y, down_pixel_y


def center_calibration(center_coordinate, width, height, pix):
    (x, y) = center_coordinate
    x = int(x)
    y = int(y)

    left_x, right_x, up_y, down_y = red_edge_detection(pix,x,y)

    center_x = int((left_x + right_x) / 2)
    center_y = int((up_y + down_y) / 2)
    return center_x, center_y


def enhance_contrast(image):
    # im = Image.open(image)
    ImageEnhance.Contrast(image).enhance(1.5)
    return image


def preprocess_image(image, center_coordinate):
    im = enhance_contrast(image)
    pix = im.load()

    (width, height) = im.size
    (x, y) = center_calibration(center_coordinate, width, height, pix)

    left_x, right_x, up_y, down_y = red_edge_detection(pix,x,y)

    try:
        img1 = im.convert("L")
        img1.crop((left_x, up_y, right_x, down_y)).save("cropped.ppm")
        binary_img = apply_otsu_algorithm("cropped.ppm")
        binary_img.save("binary.ppm")
        return Image.open("binary.ppm")
    except:
        raise WrongCenterException
