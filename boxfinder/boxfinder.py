from PIL import Image
from PIL import ImageEnhance

def is_pixel_red (r, g, b):
    if (r > 80 and 15 > g and 15 > b):
        return True
    elif (r > 80 and g == 0 and b == 0):
        return True
    elif ((g + b) < (r / 2) and r > 100):
        return True
    else:
        return False

def red_right (pix, x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x += 1

def red_left (pix, x, y):
    for i in range(x-1):
        (r, g, b) = pix[x, y]
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x -= 1    

def red_up (pix, x, y):
    for i in range(y-1):
        (r, g, b) = pix[x, y]
        if (is_pixel_red(r, g, b) == True):
            return x, y
        y -= 1

def red_bottom (pix, x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        y += 1

def distance_to_right_edge (center_x, width):
    return width - center_x

def distance_to_bottom_edge (center_y, height):
    return height - center_y

def find_box(pix, x, y, width, height):
    #Calculates the distances to the edges of the image
    right_edge_distance = distance_to_right_edge (x, width)
    bottom_edge_distance = distance_to_bottom_edge (y, height)

    #Finds the first red pixel to the left, right, up and down
    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)

    #sets the start coordinate to the top left corner by combining the left most red pixels x coordinate with the highest most red pixels y coordinate
    (start_x, start_y) = (left_red_x, up_red_y)

    x_origin = start_x

    #Initializing 4 coordinates which will be used to store the coordinates for the black pixels
    (top_most_x, top_most_y) = (x, y)
    (bottom_most_x, bottom_most_y) = (x, y)
    (right_most_x, right_most_y) = (x, y)
    (left_most_x, left_most_y) = (x, y)

    #Runs through every pixel in the detected speed sign and finds the top most, left most, right most and bottom most black pixel
    for i in range(bottom_red_y - up_red_y):
        for k in range(right_red_x - left_red_x):
            if (pix[start_x, start_y] == (0, 0, 0)):
                if (start_y < top_most_y):
                    (top_most_x, top_most_y) = (start_x, start_y)
                    continue

                if (start_y > bottom_most_y):
                    (bottom_most_x, bottom_most_y) = (start_x, start_y)
                    continue

                if (start_x > right_most_x):
                    (right_most_x, right_most_y) = (start_x, start_y)
                    continue

                if (start_x < left_most_x):
                    (left_most_x, left_most_y) = (start_x, start_y)
                    continue
                
            start_x += 1
        start_x = x_origin
        start_y += 1

    #Creates a square, surrounding all the numbers in the speed sign
    top_left_corner = (left_most_x, top_most_y)
    bottom_left_corner = (left_most_x, bottom_most_y)
    top_right_corner = (right_most_x, top_most_y)
    bottom_right_corner = (right_most_x, bottom_most_y)

    print (top_left_corner, bottom_left_corner, top_right_corner, bottom_right_corner)

    return left_most_x, top_most_y, right_most_x, bottom_most_y

def centrum_calibration(x, y, width, height, pix):
    right_edge_distance = distance_to_right_edge (x, width)
    bottom_edge_distance = distance_to_bottom_edge (y, height)

    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)
    
    center_x = int((left_red_x + right_red_x)/2)
    center_y = int((up_red_y + bottom_red_y)/2)
    return center_x, center_y
    
def return_coordinates(image, center_coordinate):
    im = Image.open(image)

    #Enhances the contrast in the image
    im2 = ImageEnhance.Contrast(im)
    im2.enhance(1.5).save("contraster1.ppm")

    im = Image.open("contraster1.ppm")
    pix = im.load()
    
    (width, height) = im.size
    (x, y) = center_coordinate
    (x, y) = centrum_calibration(x, y, width, height, pix)

    #returns the needed coordinates for cropping an image
    (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = find_box(pix, x, y, width, height)

    #crops the image and saves it as a new image, only containing the numbers in the speed sign with 1 extra pixel on each side.
    cropped = im.crop((top_left_x - 1, top_left_y - 1, bottom_right_x + 1, bottom_right_y + 1))
    cropped.save("cropped final.ppm")
        
