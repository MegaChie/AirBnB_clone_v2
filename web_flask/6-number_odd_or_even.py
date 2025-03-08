#!/usr/bin/python3
"""Script that starts a Flask web application:\
        listening on 0.0.0.0, port 5000"""

from flask import Flask, render_template

app = Flask(__name__)

# Define a route that displays "Hello HBNB!"


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

# Define a route that displays "HBNB"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

# Define a route that takes a text variable.


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')
    return "C " + text

# Define a route that takes a text variable.
# If no text is provided, use the default value "is cool"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "Python " + text

# Define a route that takes an integer:
# and displays "n is a number" only if n is an integer


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return "{} is a number".format(n)

# Define a route that takes an integer and:
# displays a template if n is an integer


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('6-number.html', n=n)

# Define a route that takes an integer:
# and displays whether it's even or odd in a template


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    if n % 2 == 0:
        even_or_odd = "even"
    else:
        even_or_odd = "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, even_or_odd=even_or_odd)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
