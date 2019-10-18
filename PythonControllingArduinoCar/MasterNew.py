def change_motor_speed(serial, data):
    byte = str(data).encode('utf-8')
    serial.write(byte)
