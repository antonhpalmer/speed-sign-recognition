from PIL import Image
from PIL import ImageEnhance
from ColorRecognizor import color_recognizor
from ColorRecognizor import black_validator
from ColorRecognizor import gray_validator
from ColorRecognizor import rgb_to_hsv
import math
import numpy


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


def remove_last_digit(pix, top_y, bottom_y, right_x, left_x):
    # Works by finding the three areas of the last digit; the right black line, the white space, and the left black line
    first_line_detected = False
    white_space_detected = False
    last_line_detected = False

    search_range = right_x - left_x
    start_x = right_x
    start_y = abs(int((top_y + bottom_y) / 2))
    black_pixel = False
    for i in range(search_range):
        if black_validator(start_x, start_y, pix):
            black_pixel = True
        else:
            black_pixel = False

        if first_line_detected is False and black_pixel is True:
            first_line_detected = True

        if first_line_detected is True and white_space_detected is False and black_pixel is False:
            white_space_detected = True

        if white_space_detected is True and black_pixel is True:
            last_line_detected = True

        if last_line_detected and black_pixel is False:
            return start_x
        start_x -= 1


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
    print((right_red_x, right_red_y), (left_red_x, left_red_y), (up_red_x, up_red_y), (bottom_red_x, bottom_red_y))

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
    # Loads the original image with enhanced color contrast
    im = Image.open(enhance_contrast(image))
    pix = im.load()

    # Loads the original image but gray scaled
    img1 = im.convert("L")
    pix_gray = img1.load()

    # Gets the dimensions of the image and calibrates the center of the speed sign
    (width, height) = im.size
    (x, y) = center_calibration(center_coordinate, width, height, pix)

    # Calculates the distances to the edges of the image from the new center of the image
    right_edge_distance = distance_to_right_edge(x, width)
    bottom_edge_distance = distance_to_bottom_edge(y, height)

    # Finds the first red pixel to the left, right, up and down
    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)

    print((right_red_x, right_red_y), (left_red_x, left_red_y), (up_red_x, up_red_y), (bottom_red_x, bottom_red_y))
    diameter = ((right_red_x - left_red_x) + (bottom_red_y - up_red_y)) / 2

    # Initializing 4 coordinates which will be used to store the coordinates for the black pixels
    (top_most_x, top_most_y) = (x, y)
    (bottom_most_x, bottom_most_y) = (x, y)
    (right_most_x, right_most_y) = (x, y)
    (left_most_x, left_most_y) = (x, y)

    # sets the start coordinate to the top left corner by combining the left most red pixels x coordinate with the
    # highest most red pixels y coordinate
    (start_x, start_y) = (left_red_x, up_red_y)

    # Saves the original values
    x_origin = start_x
    y_origin = start_y

    # Runs through every pixel in the detected speed sign and finds the top most, left most, right most and bottom
    # most black pixel
    for i in range(bottom_red_y - y_origin):
        for k in range(right_red_x - x_origin):
            r,g,b = pix[start_x,start_y]
            if black_validator(start_x, start_y, pix_gray) and is_point_within_circle(x, y, diameter, start_x, start_y) and color_recognizor(r,g,b) != "Red":
                if start_y < top_most_y:
                    (top_most_x, top_most_y) = (start_x, start_y)

                if start_y > bottom_most_y:
                    (bottom_most_x, bottom_most_y) = (start_x, start_y)

                if start_x > right_most_x:
                    (right_most_x, right_most_y) = (start_x, start_y)

                if start_x < left_most_x:
                    (left_most_x, left_most_y) = (start_x, start_y)

            start_x += 1
        start_x = x_origin
        start_y += 1

    print((right_most_x, right_most_y), (left_most_x, left_most_y), (top_most_x, top_most_y),
          (bottom_most_x, bottom_most_y))
    # Marks the x value in which to crop to remove the last digit from the speed sign
    right_x = remove_last_digit(pix_gray, top_most_y, bottom_most_y, right_most_x, left_most_x)
    print(right_x)
    if right_x is None:
        return 0

    # Arrayet
    start_x, start_y = (left_most_x, bottom_most_y)
    x_origin = start_x
    y_origin = start_y

    pixels = []
    bottom_y = None
    for i in range(bottom_most_y - top_most_y):
        for k in range(right_x - left_most_x):
            pixels.append(1) if black_validator(start_x, start_y, pix_gray) else pixels.append(0)
            start_x += 1

        clean_row = any(elem == 1 for elem in pixels)
        if clean_row is False:
            bottom_y = start_y
            break
        pixels.clear()
        start_x = x_origin
        start_y -= 1
    if bottom_y is None:
        bottom_y = y_origin

    # Colors the image black/white without noise
    #perfect_image(pix_gray, left_most_x, top_most_y, bottom_y, right_x)

    # Crops the image and saves it as a new image, only containing the numbers in the speed sign with 1 extra pixel
    # on each side.
    if right_x != None and left_most_x != right_x and top_most_y != bottom_y:
        cropped = img1.crop((left_most_x, top_most_y, right_x, bottom_y))
        cropped.save(
            "C:/Users/frede/OneDrive/Dokumenter/GitHub/speed-sign-recognition/test_data/training_images_digits/8/" + filename)
    else:
        print("Image failed:", image)


def perfect_image(pix_gray, top_left_x, top_left_y, bottom_right_y, bottom_right_x):
    x_origin = top_left_x
    start_x = x_origin
    start_y = top_left_y
    for i in range(bottom_right_y - top_left_y):
        for k in range(bottom_right_x - top_left_x):
            if black_validator(start_x, start_y, pix_gray):
                pix_gray[start_x, start_y] = 0
            else:
                pix_gray[start_x, start_y] = 255
            start_x += 1
        start_x = x_origin
        start_y += 1
