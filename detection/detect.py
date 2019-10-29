from detection.pixy_serial_communication.pixy_snapper import get_cropped_image
from detection.pixy_serial_communication.serial_reader import get_serial_data


def detect(ser):
    x, y, w, h = get_serial_data(ser)
    print("x:", x, "y:", y, "w:", w, "h:", h)
    img = get_cropped_image(int(x), int(y), int(w), int(h))
    return img
