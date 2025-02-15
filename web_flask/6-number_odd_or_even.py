#!/usr/bin/python3
"""
   simple flask app

"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbn():
    """ intro """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ name """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ display C followed by text """
    return f"C {text.replace('_', ' ')}"

@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """ display Python followed by text """
    return f"Python {text.replace('_', ' ')}"

@app.route('/number/<int:n>', strict_slashes=False)
def display_n(n):
    """ display n is number when n is integer """
    return f"{n} is a number"

@app.route('/number_template/<int:n>', strict_slashes=False)
def html_page(n):
    """ render page when n is integer """
    return render_template('5-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def html_page_2(n):
    """ render page when n is integer """
    x = "even" if (n % 2) == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n, x=x)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
