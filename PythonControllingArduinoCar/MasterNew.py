import serial

arduinoData = serial.Serial('/dev/ttyACM1', 115200)


def speed_zero():
    arduinoData.write(b'0')


def speed_one():
    arduinoData.write(b'1')


def speed_two():
    arduinoData.write(b'2')


def speed_three():
    arduinoData.write(b'3')


def speed_four():
    arduinoData.write(b'4')


def speed_five():
    arduinoData.write(b'5')


def speed_six():
    arduinoData.write(b'6')


def speed_seven():
    arduinoData.write(b'7')


def stop_motor():
    arduinoData.write(b'8')


def change_motor_speed(data):
    x = data

    if x == 0:
        speed_zero()
        print("speed: 20")
    elif x == 1:
        speed_one()
        print("speed: 30")
    elif x == 2:
        speed_two()
        print("speed: 50")
    elif x == 3:
        speed_three()
        print("speed: 60")
    elif x == 4:
        speed_four()
        print("speed: 70")
    elif x == 5:
        speed_five()
        print("speed: 80")
    elif x == 6:
        speed_six()
        print("speed: 100")
    elif x == 7:
        speed_seven()
        print("speed: 120")
