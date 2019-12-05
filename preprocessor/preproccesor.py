from PIL import Image
from PIL import ImageEnhance
from preprocessor.color_recognizor import red_validator, is_pixel_red
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
            pass

    return red_pixels


def get_neighbours(current_pixel):
    x = current_pixel[0]
    y = current_pixel[1]
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return neighbours


def detect_red_cluster(image, current_pixel, cluster, closed_set):
    neighbours = get_neighbours(current_pixel)

    for neighbour in neighbours:
        try:
            if neighbour not in closed_set:
                closed_set.append(neighbour)
                if is_pixel_red(current_pixel, image) is True:
                    cluster.append(neighbour)
                    if len(cluster) >= 10:
                        return cluster, closed_set
                    cluster, closed_set = detect_red_cluster(image, neighbour, cluster, closed_set)
        except IndexError:
            pass  # Happens when we try to get a neighbour outside the image

    return cluster, closed_set


def check_current_pixel(x, y, image):
    current_pixel = (x, y)
    if is_pixel_red(current_pixel, image) is True:
        cluster = [current_pixel]
        closed_set = [current_pixel]
        cluster, closed_set = detect_red_cluster(image, current_pixel, cluster, closed_set)
        if len(cluster) >= 10:
            return True

    return False


def red_right(image, x, y, loop_range):
    for i in range(loop_range):
        try:
            if (check_current_pixel(x, y, image)) is True:
                return x
            x += 1
        except IndexError:
            print("No red pixel found to the right")
    return x


def red_left(image, x, y):
    for i in range(x - 1):
        try:
            if (check_current_pixel(x, y, image)) is True:
                return x
            x -= 1
        except IndexError:
            print("No red pixel found to the left")
    return x


def red_up(image, x, y):
    for i in range(y - 1):
        try:
            if (check_current_pixel(x, y, image)) is True:
                return y
            y -= 1
        except IndexError:
            print("No red pixel found upwards")
    return y


def red_bottom(image, x, y, loop_range):
    for i in range(loop_range):
        try:
            if (check_current_pixel(x, y, image)) is True:
                return y
            y += 1
        except IndexError:
            print("No red pixel found in the bottom")
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


def enhance_contrast(image):
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


def preprocess_image_test(image_path, given_center_coordinate):
    image = Image.open(image_path)
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

