import sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
import time

board = CustomPymata4(com_port="COM3")
MAX_ANGLE = 360
POT_PIN = 0


def get_angle(data):
    sensor_value = data[2]
    angle = sensor_value * MAX_ANGLE / 1023.0
    print(f"angle: {angle:.1f}")
   # board.displayShow(angle)


DHTPIN = 12


def setup():
    global board
    board = CustomPymata4(com_port="COM3")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)


def loop():
    humidity, temperature, timestamp = board.dht_read(DHTPIN)
    print(humidity, temperature)
    board.displayShow(temperature)
    time.sleep(0.01)


#board.set_pin_mode_analog_input(POT_PIN, callback=get_angle, differential=10)
setup()
while True:
    try:
        loop()
    except KeyboardInterrupt: # crtl+C
        print ('shutdown')
        board.shutdown()
        sys.exit(0)
    time.sleep(0.05)

    