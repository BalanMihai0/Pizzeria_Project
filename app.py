import datetime
import time
import csv
import json
from xmlrpc.client import MININT, MAXINT
from fhict_cb_01.CustomPymata4 import CustomPymata4
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DHTPIN = 12  # digital pin
LDRPIN = 2

sensor1_data = []
# 0-3 temperature , 4-7 humidity, 8-11 light
# order: min, max, avg, last
# setup of list
i = 0
while i < 50:
    sensor1_data.append(0)
    i += 1
def Measure(data):
    global humidity, temperature
    if data[3] == 0:
        humidity = data[4]
        temperature = data[5]
def Measure_light(data):
    global light
    light = data[2]
def setup():
    global board
    board = CustomPymata4(com_port="COM4")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=0.05, callback=Measure)
    board.set_pin_mode_analog_input(LDRPIN, callback=Measure_light, differential=10)

# number of measurements


@app.route("/")


@app.route("/asdfg", methods=['POST']) 
  
@app.route("/register", methods=['POST'])
