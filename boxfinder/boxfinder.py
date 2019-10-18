from PIL import Image

#READ! : Just call 'return_coordinates' with appropriate input and it does the job.

#returns True if pixel is red, False if pixel is not red.
def is_pixel_red (r, g, b):
    if (r >= 200 & (g + b) <= 150):
        return True
    elif (r >= 150 & (g + b) <= 100):
        return True
    else:
        return False

#returns x, y coordinates
def top_left (pix, x, y, loop):
    for i in range(loop):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x += 1
        y += 1

#returns x, y coordinates
def top_right (pix, x, y, loop):
    for i in range(loop):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x += 1
        y -= 1    

#returns x, y coordinates
def bottom_left (pix, x, y, loop):
    for i in range(loop):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x -= 1
        y += 1

#returns x, y coordinates
def bottom_right (pix, x, y, loop):
    for i in range(loop):
        (r, g, b) = pix[x, y]
    
        if (is_pixel_red(r, g, b) == True):
            return x, y
        x -= 1
        y -= 1

def loop_range (center_x, center_y, width, height):
    if center_x >= center_y:
        return height - center_y 
    elif center_y > center_x:
        return width - center_x


def return_coordinates(image, center_coordinate):
    im = Image.open(image)
    pix = im.load()
    
    (width, height) = im.size
    (x, y) = center_coordinate
    
    loop = loop_range(x, y, width, height)
    corner_top_left = top_left(pix, x, y, loop)
    corner_top_right = top_right(pix, x, y, loop)
    corner_bottom_left = bottom_left(pix, x, y, loop)
    corner_bottom_right = bottom_right(pix, x, y, loop)
    
    return corner_top_left, corner_top_right, corner_bottom_left, corner_bottom_right
