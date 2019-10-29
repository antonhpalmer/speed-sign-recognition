def color_recognizor(r,g,b):
    h,s,v = rgb_to_hsv(r,g,b)

    if (white_validator(s,v) == True):
        return "White"
    elif(red_validator(h,s,v) == True):
        return "Red"
    #elif(black_validator(s,v) == True):
    #    return "Black"
    else:
        return "Black"

def black_validator(s,v):
    s_bound = 50
    v_bound = 40

    if (v < v_bound and s > s_bound):
        return True
    else:
        return False

def white_validator(s,v):
    s_bound = 50
    v_bound = 50

    if (v > v_bound and s < s_bound):
        return True
    else:
        return False

def red_validator(h,s,v):
    red1_lower = [0, 75, 40]
    red1_upper = [10, 100, 100]

    red2_lower = [330, 75, 30]
    red2_upper = [360, 100, 100]


    if (is_value_between(h, red1_lower[0], red1_upper[0]) and
            is_value_between(s, red1_lower[1], red1_upper[1]) and
            is_value_between(v, red1_lower[2], red1_upper[2])):
        return True
    elif (is_value_between(h, red2_lower[0], red2_upper[0]) and
            is_value_between(s, red2_lower[1], red2_upper[1]) and
            is_value_between(v, red2_lower[2], red2_upper[2])):
        return True
    else:
        return False


def is_value_between(check, lower_bound, upper_bound):
    if (check >= lower_bound and check <= upper_bound):
        return True
    else:
        return False

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v