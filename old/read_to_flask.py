import datetime
import time
import sys
import ast
import inspect
import csv
from fhict_cb_01.CustomPymata4 import CustomPymata4
from flask import Flask, render_template

app = Flask(__name__)
with open('measurements.csv','r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            print(lines)


#if __name__ == "__main__":
   # app.run()