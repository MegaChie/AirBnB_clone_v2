#!/usr/bin/python3
"""
   simple flask app

"""

from flask import Flask

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

@app.route('/number/<n>', strict_slashes=False)
def display_n(n):
    """ display n is number when n is integer """
    if isinstance(n, int):
        return f"{n} is a number"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
