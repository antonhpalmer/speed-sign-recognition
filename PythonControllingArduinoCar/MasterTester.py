import serial
from classification.test.test import ModelTester
from keras.models import load_model

arduino_data = serial.Serial('com5', 115200)
mg_one = "C:/Users/anton/PycharmProjects/speed-sign-recognition/GTSRB/Final_Training/Images/00000/00000_00000.ppm"
img_two = "C:/Users/anton/PycharmProjects/speed-sign-recognition/GTSRB/Final_Test/Images/00011.ppm"

def speed_zero():
    arduino_data.write(b'0')


def speed_one():
    arduino_data.write(b'1')


def speed_two():
    arduino_data.write(b'2')


def speed_three():
    arduino_data.write(b'3')


def speed_four():
    arduino_data.write(b'4')


def speed_five():
    arduino_data.write(b'5')


def speed_six():
    arduino_data.write(b'6')


def speed_seven():
    arduino_data.write(b'7')


def stop_motor():
    arduino_data.write(b'8')

def control_speed(sign_class_id):
    if sign_class_id == 0:
        speed_zero()
        print("speed: 20")
    elif sign_class_id == 1:
        speed_one()
        print("speed: 30")
    elif sign_class_id == 2:
        speed_two()
        print("speed: 50")
    elif sign_class_id == 3:
        speed_three()
        print("speed: 60")
    elif sign_class_id == 4:
        speed_four()
        print("speed: 70")
    elif sign_class_id == 5:
        speed_five()
        print("speed: 80")
    elif sign_class_id == 6:
        speed_six()
        print("speed: 100")
    elif sign_class_id == 7:
        speed_seven()
        print("speed: 120")
