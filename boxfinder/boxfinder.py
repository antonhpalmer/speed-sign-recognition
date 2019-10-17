from PIL import Image

#returns True if pixel is red, False if pixel is not red.
def is_pixel_red (r, g, b):
    if (r >= 200 & (g + b) <= 150):
        return True
    elif (r >= 150 & (g + b) <= 100):
        return True
    else:
        return False

#returns x, y coordinates
def top_left (x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x += 1
        y += 1

#returns x, y coordinates
def top_right (x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x += 1
        y -= 1    

#returns x, y coordinates
def bottom_left (x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x -= 1
        y += 1

#returns x, y coordinates
def bottom_right (x, y, loop_range):
    for i in range(loop_range):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x -= 1
        y -= 1

def loop_range (center_x, center_y, width, height)
    if center_x >= center_y:
        return height - center_y 
    elif center_y > center_x:
        return width - center_x


def return_coordinates(image, center_coordinate):
    pix = image.load()
    
    (width, height) = image.size
    (x, y) = center_coordinate
    
    loop_range = loop_range(x, y, width, height)
    
    corner_top_left = top_left(x, y, loop_range)
    corner_top_right = top_right(x, y, loop_range)
    corner_bottom_left = bottom_left(x, y, loop_range)
    corner_bottom_right = bottom_right(x, y, loop_range)
    
    print (corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right)
