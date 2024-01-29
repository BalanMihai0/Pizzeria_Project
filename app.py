import datetime
import time
import csv
import json
import re
import random
from random import randint
from xmlrpc.client import MININT, MAXINT
from fhict_cb_01.CustomPymata4 import CustomPymata4
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
#import flask_sqlalchemy
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'thisisasecretkey'
user = []


class Timer:
    def __init__(self, current_time):
        self.current_time = current_time

    def decrement(self):
        if self.current_time > 0:
            self.current_time = self.current_time - 1
        return self.current_time


t = Timer(current_time=600)


@app.route("/")
def nothing():
    return render_template('main_page.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if (request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['rpassword']
        phonenumber = request.form['phonenumber']
        if password == repassword:
            user = [username, email, phonenumber, password]
            with open('database.csv', 'a', newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(user)
            return redirect('/login')
        else:
            flash("Passwords don't match")
        return redirect('register')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        with open('database.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for lines in reader:
                if username == lines["Username"]:
                    print("got here")
                    if password == lines["Password"]:
                        print("got here 2")
                        return redirect('/')
                    else:
                        flash("Wrong password")
    return render_template('login.html')


@app.route('/kitchen')
def chef():
    id = []
    name = []
    ingredients = []
    linenumbers = []
    with open('order.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for lines in reader:
            id.append(lines["id"])
            name.append(lines["Pizza"])
            ingredients.append(lines["Ingredients"])
            linenumbers.append(lines["linenumber"])
    ordernumber = random.randint(1000, 9999)
    return render_template('kitchen.html', ids=id, names=name, ingredientss=ingredients, linenumber=linenumbers, ordernumber=ordernumber)


global countnew
countnew = 0


@app.route('/cashier')
def cashier():
    global countnew
    countnew = 0
    id = []
    name = []
    price = []
    sumprice = 0
    with open('order.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for lines in reader:
            id.append(lines["id"])
            if lines["id"] == "new":
                countnew = 1
                sumprice = 0
            name.append(lines["Pizza"])
            st = int(lines["Price"])
            conv = int(st)
            price.append(conv)
            sumprice += conv
    return render_template('cashier.html', ids=id, names=name, price=price, countnew=countnew, total=sum(price))


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/locations')
def location():
    return render_template('locations.html')


@app.route('/offers')
def offer():
    return render_template('offers.html')


@app.route('/order', methods=['POST', 'GET'])
def order():
    return render_template('order.html')


global id
id = 0
global linenumber
linenumber = 2


@app.route('/ordermarg', methods=['POST', 'GET'])
def om():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Margarita']
    print(p)
    id += 1
    ingredients = "Italian flour; whole tomato sauce; mozzarella; tomatoes; pestosauce; oregano"
    price = 10
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/ordermarak', methods=['POST', 'GET'])
def omk():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Marrakech']
    print(p)
    id += 1
    ingredients = "Italian flour; truffle sauce; mozzarella; duck fillet (sous-style); figs; brie; almonds; pomegranate sauce."
    price = 13
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/ordersal', methods=['POST', 'GET'])
def oms():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Salami']
    print(p)
    id += 1
    ingredients = "Italian flour; mozzarell;, whole tomato sauce; premium salami; oregano"
    price = 10
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/orderprosc', methods=['POST', 'GET'])
def omp():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Prosciutto']
    print(p)
    id += 1
    ingredients = "Italian flour; whole tomato sauce; mozzarella; prossuitto; arugula; cherries; sun-dried tomato; capers; oregano; parmesan"
    price = 15
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/orderbav', methods=['POST', 'GET'])
def omb():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Bavarian']
    print(p)
    id += 1
    ingredients = "Italian flour; whole tomato sauce; mozzarella; pepperoni; huntingsausages; bell pepper; olives; Pesto sauce; oregano"
    price = 12
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/orderpep', methods=['POST', 'GET'])
def ompe():
    global id
    global linenumber
    linenumber += 1
    p = request.form['Pepperoni']
    print(p)
    id += 1
    ingredients = "Italian flour; mozzarella; whole tomato sauce; real Italian pepperoni; hot pepper; capers; oregano"
    price = 10
    pizza = [linenumber, id, p, ingredients, price]
    with open('order.csv', 'a', newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        if id == 1 or id == 0:
            neworder = [linenumber, 'new', 'new', 'new', int(0)]
            csvwriter.writerow(neworder)
        csvwriter.writerow(pizza)
    return render_template('order.html')


@app.route('/payment', methods=['POST', 'GET'])
def pay():
    return render_template('payment.html')


@app.route('/paymentdone', methods=['POST', 'GET'])
def paydone():
    return redirect('/cashier')


@app.route('/deleteline', methods=['POST', 'GET'])
def delet():
    """
    ptr = request.form['linenumber']
    emptyrow = ['','','','','']
    with open('order.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for lines in reader:
            if lines['linenumber'] == ptr:
                with open('order.csv','w', newline="", encoding="utf-8") as csvfile: 
                    csvwriter = csv.writer(csvfile, delimiter=',')
                    csvwriter.writerow(emptyrow)
    """

    return redirect('/kitchen')


@app.route('/reservation')
def reserve():
    return render_template('reservation.html')


@app.route('/shopping_cart')
def shop():
    return render_template('shopping_cart.html')


@app.route('/oven')
def bake():
    choice = random.randint(205, 220)
    return render_template("oven.html", choice=choice)


if __name__ == "__main__":
    app.run(debug=True)
