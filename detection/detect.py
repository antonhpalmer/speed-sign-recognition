from detection.PixySerialCommunication.SerialReader import get_serial_data

def detect(ser):
    path = get_serial_data(ser)
    return path
