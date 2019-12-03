from PIL import Image
from PIL import ImageEnhance
from preprocessor.color_recognizor import red_validator

from preprocessor.directions import Direction
from preprocessor.no_red_pixel_exception import NoRedPixelException
from preprocessor.otsu import apply_otsu_algorithm
from preprocessor.wrong_center_exception import WrongCenterException


def get_neighbours(x, y):
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return neighbours


def check_for_red_cluster(pix, current_pixel, cluster, closed_set):
    neighbours = get_neighbours(current_pixel[0], current_pixel[1])
    closed_set.append(neighbours)

    for neighbour in neighbours:
        try:
            (r, g, b) = pix[neighbour[0], neighbour[1]]
            if neighbour not in closed_set and red_validator(r, g, b) is True:
                cluster.append(neighbour)
                if len(cluster) >= 10:
                    return cluster, closed_set
                cluster, closed_set = check_for_red_cluster(pix, neighbour, cluster, closed_set)
        except IndexError:
            pass  # Happens when we find a neighbour outside the image.

    return cluster, closed_set


def detect_red_cluster(pix, x, y):
    current_pixel = (x, y)
    (r, g, b) = pix[x, y]
    if red_validator(r, g, b) is True:
        cluster = []
        closed_set = []
        cluster.append(current_pixel)
        closed_set.append(current_pixel)
        return len(check_for_red_cluster(pix, current_pixel, cluster, closed_set))


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


def center_calibration(center_coordinate, pix):
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
