#!/usr/bin/python3

"""Script that starts a Flask web application :\
        listening to port 5000 routes:\
        /displaying "Hello HBNB" "/hbnb:“HBNB”
/c/<text>: displaying “C ”, followed by :\
        the value of the text variable
/python/(<text>) """
from flask import Flask

app = Flask(__name__)

# Define a route that displays "Hello HBNB!"


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

# Define a route that displays "HBNB"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

# Define a route that takes a text variable


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')
    return "C " + text

# Define a route that takes a text variable
# If no text is provided, use the default value "is cool"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    text = text.replace('_', ' ')
    return "Python " + text

# Define a route that takes an integer


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return f"{n} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
