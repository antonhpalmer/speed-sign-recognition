from detection.PixySerialCommunication.SerialReader import get_serial_data

def detect():
    path = get_serial_data(115200)
    return path


detect()
