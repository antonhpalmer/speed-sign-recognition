from PIL import Image
from PIL import ImageEnhance
from ColorRecognizor import color_recognizor
import math


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
            if color_recognizor(r, g, b) == "Red" and (x, y) not in red_pixels:
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
            if color_recognizor(r, g, b) == "Red":
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x, y
            red_pixel_list.clear()
            x += 1
        except IndexError:
            print("pixel out of bounds")
    return x, y


def red_left(pix, x, y):
    red_pixel_list = []
    for i in range(x - 1):
        try:
            (r, g, b) = pix[x, y]
            if color_recognizor(r, g, b) == "Red":
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x, y
            red_pixel_list.clear()
            x -= 1
        except IndexError:
            print("index out of bounds")
    return x, y


def red_up(pix, x, y):
    red_pixel_list = []
    for i in range(y - 1):
        try:
            (r, g, b) = pix[x, y]
            if color_recognizor(r, g, b) == "Red":
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x, y
            red_pixel_list.clear()
            y -= 1
        except IndexError:
            print("index out of bounds")
    return x, y


def red_bottom(pix, x, y, loop_range):
    red_pixel_list = []
    for i in range(loop_range):
        try:
            (r, g, b) = pix[x, y]
            if color_recognizor(r, g, b) == "Red":
                red_pixel_list.append((x, y))
                l = len(check_neighbour_pixels(pix, x, y, red_pixel_list))
                if l > 10:
                    return x, y
            red_pixel_list.clear()
            y += 1
        except IndexError:
            print("out of bounds")
    return x, y


def distance_to_right_edge(center_x, width):
    return width - center_x


def distance_to_bottom_edge(center_y, height):
    return height - center_y


def center_calibration(center_coordinate, width, height, pix):
    (x, y) = center_coordinate
    x = int(x)
    y = int(y)
    right_edge_distance = distance_to_right_edge(x, width)
    bottom_edge_distance = distance_to_bottom_edge(y, height)

    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)

    center_x = int((left_red_x + right_red_x) / 2)
    center_y = int((up_red_y + bottom_red_y) / 2)
    return center_x, center_y


def is_point_within_circle(center_x, center_y, diameter, pixel_x, pixel_y):
    # pythagoras to determine whether or not a given point is within the red circle.
    radius = int(diameter / 2) - 1
    distance = math.sqrt((pixel_x - center_x) ** 2 + (pixel_y - center_y) ** 2)
    return distance < radius


def enhance_contrast(image):
    im = Image.open(image)
    im2 = ImageEnhance.Contrast(im)
    im2.enhance(1.5).save("contraster1.ppm")

    return "contraster1.ppm"


def crop_image(image, center_coordinate, filename):
    im = Image.open(enhance_contrast(image))
    pix = im.load()

    img1 = im.convert("L")

    (width, height) = im.size
    (x, y) = center_calibration(center_coordinate, width, height, pix)

    right_edge_distance = distance_to_right_edge(x, width)
    bottom_edge_distance = distance_to_bottom_edge(y, height)

    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)

    couldnt_crop = 0
    could_crop = 0
    try:
        cropped = img1.crop((left_red_x, up_red_y, right_red_x, bottom_red_y))
        cropped.save(
            "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images_gray/8/" + filename)
        could_crop += 1
    except:
        couldnt_crop += 1

    return could_crop, couldnt_crop
