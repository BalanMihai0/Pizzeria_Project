import datetime
import time
import csv
import json
from xmlrpc.client import MININT, MAXINT
from fhict_cb_01.CustomPymata4 import CustomPymata4

global board 
board = CustomPymata4(com_port="COM4")
LED_PINS=[4,5,6,7]
RIGHTBUTTON = 8
LEFTBUTTON = 9
BUTTON_PRESSED = 0
MAX_ANGLE = 280
POT_PIN = 0
BUZZER = 3

board.set_pin_mode_digital_input_pullup(RIGHTBUTTON)
board.set_pin_mode_digital_input_pullup(LEFTBUTTON)
time.sleep(0.5)
board.displayOn()

def timer():
    finish = False
    i=600
    while i>0 :
        starttimer = board.digital_read(RIGHTBUTTON)
        time.sleep(0.02)
        if (starttimer[0] == BUTTON_PRESSED) :
            board.digital_pin_write(LED_PINS[1], 0)
            #start oven
            #pizza takes 10 minutes to cook or idk
            i=600 #in seconds
            finish = False
            while i>0 and not finish: 
                skip = board.digital_read(LEFTBUTTON)
                if(skip[0] == BUTTON_PRESSED):
                    finish = True
                board.displayShow(i)
                time.sleep(1)
                i-=1
            board.displayShow("done")
            board.digital_write(BUZZER, 0)
        else:
            board.digital_pin_write(LED_PINS[0], 0) 

def settemp(data):
    sensor_value= data[2]
    temperature = sensor_value * MAX_ANGLE/1023
    print(temperature)
    board.displayShow(temperature) 

if not(board.digital_read(RIGHTBUTTON) == BUTTON_PRESSED or board.digital_read(LEFTBUTTON) == BUTTON_PRESSED) :
    board.set_pin_mode_analog_input(POT_PIN, callback = settemp, differential = 10)
timer()