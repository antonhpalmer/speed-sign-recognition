from detection.PixySerialCommunication.PixySnapper import get_cropped_image
from detection.PixySerialCommunication.SerialReader import get_serial_data


def detect(ser):
    x, y, w, h = get_serial_data(ser)
    print("x:", x, "y:", y, "w:", w, "h:", h)
    img = get_cropped_image(int(x), int(y), int(w), int(h))
    return img
