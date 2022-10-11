from flask import Flask
from flask import render_template
import datetime
app = Flask(__name__)

"""
@app.route('/')
def hw():
    return "<p>Hello world</p>"


@app.route('/mary')
def hwm():
    return "<p>Hello mary</p>"
"""
@app.route('/')
def with_template():
    return render_template('general.html',  people_names = ['mary', 'john', 'sonic'],  time = datetime.datetime.now())

