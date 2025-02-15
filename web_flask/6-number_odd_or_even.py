#!/usr/bin/python3
"""starts a Flask web application"""


from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def flask_hello():
    """Return string response"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return response"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def text(text):
    """Replace underscores with spaces in the text"""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def fl_python(text="is cool"):
    """Replace underscores with spaces,else use default"""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route('/number/<int:n>')
def number(n):
    """Return "{} is a number" with the value of n"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def html(n):
    """Displays HTML page if n is an int"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Displays HTML page if n is an int"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
