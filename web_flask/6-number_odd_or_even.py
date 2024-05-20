#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """displays Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def showc(text):
    """displays "C" followed by value of text"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/pyton/<text>', strict_slashes=False)
def showpyhton(text='is cool'):
    """displays "Python" followed by value of text"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<n>', strict_slashes=False)
def shownumber(n):
    """displays "n is a number" only if n is an integer"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<n>', strict_slashes=False)
def numbertemplates(n):
    """displays a HTML pahe only if n is an integer"""
    return render_templates('5-number.html', n=n)


@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def oddoreven(n):
    """displays a HTML page only if n is an integer"""
    if n % 2 == 0:
        evenness = 'even'
    else:
        evenness = 'odd'
    return render_template('6-number_odd_or_even.html', n=n, evenness=evenness)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
