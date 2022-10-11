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

class Reading:
    def __init__(self, temp, hum, li):
        self.temperature=temp
        self.humidity = hum
        self.brightness = li
        Reading.add_reading()
    @classmethod
    def add_reading(cls):
        cls.numberOfReadings +=1
    @classmethod
    def get_number_readings(cls):
        return cls.numberOfReadings


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


def get_min(list):
    min_list = MAXINT
    for i in range(0, len(list)):
        if list[i] < min_list:
            min_list = list[i]
    return min_list


def get_max(list):
    max_list = MININT
    for i in range(0, len(list)):
        if list[i] > max_list:
            max_list = list[i]
    return max_list

temps = []
hums = []
lis = []
# number of measurements


@app.route("/")
def display_air():
    time.sleep(0.5)
    humidity, temperature, timestamp = board.dht_read(DHTPIN)
    light, timestamp = board.analog_read(LDRPIN)
    temps.append(temperature)
    hums.append(humidity)
    lis.append(light)
    # temperature
    sensor1_data[0] = get_min(temps)
    sensor1_data[1] = get_max(temps)
    sensor1_data[2] = sum(temps) / len(temps)
    sensor1_data[3] = temperature
    # humidity
    sensor1_data[4] = get_min(hums)
    sensor1_data[5] = get_max(hums)
    sensor1_data[6] = sum(hums) / len(hums)
    sensor1_data[7] = humidity
    # light
    sensor1_data[8] = get_min(lis)
    sensor1_data[9] = get_max(lis)
    sensor1_data[10] = sum(lis) / len(lis)
    sensor1_data[11] = light
    board.displayShow(temperature)
    # showing values
    fields = [datetime.datetime.now(), temperature, humidity, light]
    with open('measurements.csv','a', newline="", encoding="utf-8") as csvfile: 
        csvwriter = csv.writer(csvfile, delimiter=',') 
        csvwriter.writerow(fields) 
    return render_template(
        "data.html",
        average_temperature=round(sensor1_data[2],2),
        average_humidity=round(sensor1_data[6],2),
        average_light=round(sensor1_data[10],2),
        timestamp=datetime.datetime.now(),
        mintemp=sensor1_data[0],
        maxtemp=sensor1_data[1],
        minhum=sensor1_data[4],
        maxhum=sensor1_data[5],
        maxlight=sensor1_data[9],
        minlight=sensor1_data[8],
        last_temp=sensor1_data[3],
        last_hum=sensor1_data[7],
        last_light=sensor1_data[11],
    )
setup()

@app.route("/asdfg", methods=['POST']) 
def receive_data():
    json_data = request.json
    return "OK", 200
    
@app.route("/register", methods=['POST'])
def recieve_user():
    global data 
    data = request.form['test_data']
    print("Recieved", data, type(data))

    #fields = [datetime.datetime.now(), temperature, humidity, light]
    with open('external_data.txt','a', newline="") as textfile: 
        textfile.write(data)
    return redirect('/')

