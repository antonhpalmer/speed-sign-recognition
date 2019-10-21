from PIL import Image
from PIL import ImageEnhance

def is_pixel_red (r, g, b):
    if (r > 30 and 10 > g and 10 > b):
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
    right_edge_distance = distance_to_right_edge (x, width)
    bottom_edge_distance = distance_to_bottom_edge (y, height)

    (right_red_x, right_red_y) = red_right(pix, x, y, right_edge_distance)
    (left_red_x, left_red_y) = red_left(pix, x, y)
    (up_red_x, up_red_y) = red_up(pix, x, y)
    (bottom_red_x, bottom_red_y) = red_bottom(pix, x, y, bottom_edge_distance)

    (start_x, start_y) = (left_red_x, up_red_y)
    x_origin = start_x

    (top_most_x, top_most_y) = (x, y)
    (bottom_most_x, bottom_most_y) = (x, y)
    (right_most_x, right_most_y) = (x, y)
    (left_most_x, left_most_y) = (x, y)

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
            
    top_left_corner = (left_most_x, top_most_y)
    bottom_left_corner = (left_most_x, bottom_most_y)
    top_right_corner = (right_most_x, top_most_y)
    bottom_right_corner = (right_most_x, bottom_most_y)

    print (top_left_corner, bottom_left_corner, top_right_corner, bottom_right_corner)

    return left_most_x, top_most_y, right_most_x, bottom_most_y

            
def return_coordinates(image, center_coordinate):
    im = Image.open(image)
    pix = im.load()
    (width, height) = im.size
    (x, y) = center_coordinate

    #imc = im
    #im1 = ImageEnhance.Brightness(imc)
    #im1.enhance(2).save("brigther.ppm")
    
    #im2 = ImageEnhance.Sharpness(imc)
    #im2.enhance(4).save("sharper.ppm")
    
    #im3 = ImageEnhance.Contrast(imc)
    #im3.enhance(1.5).save("contraster.ppm")

    #im4 = ImageEnhance.Color(imc)
    #im4.enhance(1.5).save("colorer.ppm")
    
    (top_left_x, top_left_y, bottom_right_x, bottom_right_y) = find_box(pix, x, y, width, height)
    
    cropped = im.crop((top_left_x - 1, top_left_y - 1, bottom_right_x + 1, bottom_right_y + 1))
    cropped.save("cropped final.ppm")
        
