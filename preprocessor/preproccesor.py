from PIL import Image
from PIL import ImageEnhance
from preprocessor.color_recognizor import red_validator
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


def red_right(pix, x, y, loop_range):
    red_pixel_list = []
    for i in range(loop_range):
        try:
            (r, g, b) = pix[x, y]
            if red_validator(r, g, b) is True:
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x
            red_pixel_list.clear()
            x += 1
        except IndexError:
            print("pixel out of bounds")
    return x


def red_left(pix, x, y):
    red_pixel_list = []
    for i in range(x - 1):
        try:
            (r, g, b) = pix[x, y]
            if red_validator(r, g, b) is True:
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x
            red_pixel_list.clear()
            x -= 1
        except IndexError:
            print("index out of bounds")
    return x


def red_up(pix, x, y):
    red_pixel_list = []
    for i in range(y - 1):
        try:
            (r, g, b) = pix[x, y]
            if red_validator(r, g, b) is True:
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return y
            red_pixel_list.clear()
            y -= 1
        except IndexError:
            print("index out of bounds")
    return y


def red_bottom(pix, x, y, loop_range):
    red_pixel_list = []
    for i in range(loop_range):
        try:
            (r, g, b) = pix[x, y]
            if red_validator(r, g, b) is True:
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return y
            red_pixel_list.clear()
            y += 1
        except IndexError:
            print("out of bounds")
    return y


def distance_to_right_edge(center_x, width):
    return width - center_x


def distance_to_bottom_edge(center_y, height):
    return height - center_y

def red_edge_detection(pix, centre_coordinate, width, height):
    (x, y) = centre_coordinate

    right_edge_distance = distance_to_right_edge(x, width)
    bottom_edge_distance = distance_to_bottom_edge(y, height)

    right_x = red_right(pix, x, y, right_edge_distance)
    left_x = red_left(pix, x, y)
    up_y = red_up(pix, x, y)
    down_y = red_bottom(pix, x, y, bottom_edge_distance)

    return right_x, left_x, down_y, up_y


def center_calibration(center_coordinate, width, height, pix):
    right_x, left_x, down_y, up_y = red_edge_detection(pix, center_coordinate, width, height)

    center_x = int((left_x + right_x) / 2)
    center_y = int((up_y + down_y) / 2)
    return center_x, center_y


def enhance_contrast(image_path):
    image = Image.open(image_path)
    ImageEnhance.Contrast(image).enhance(1.5)
    return image


def preprocess_image(image, given_center_coordinate):
    im = enhance_contrast(image)
    pix = im.load()

    (width, height) = im.size

    (x, y) = given_center_coordinate
    x = int(x)
    y = int(y)
    int_centre_coordinate = (x, y)

    new_centre_coordinate = center_calibration(int_centre_coordinate, width, height, pix)

    right_x, left_x, down_y, up_y = red_edge_detection(pix, new_centre_coordinate, width, height)

    try:
        img1 = im.convert("L")
        img1.crop((left_x, up_y, right_x, down_y)).save("cropped.ppm")
        binary_img = apply_otsu_algorithm("cropped.ppm")
        binary_img.save("binary.ppm")
        return Image.open("binary.ppm")
    except:
        raise WrongCenterException

def preprocess_image_test(image, given_center_coordinate):
    im = enhance_contrast(image)
    pix = im.load()

    (width, height) = im.size

    (x, y) = given_center_coordinate
    x = int(x)
    y = int(y)
    int_centre_coordinate = (x, y)

    new_centre_coordinate = center_calibration(int_centre_coordinate, width, height, pix)

    right_x, left_x, down_y, up_y = red_edge_detection(pix, new_centre_coordinate, width, height)

    try:
        img1 = im.convert("L")
        img1.crop((left_x, up_y, right_x, down_y)).save("cropped.ppm")
        return apply_otsu_algorithm("cropped.ppm")
    except:
        pass

