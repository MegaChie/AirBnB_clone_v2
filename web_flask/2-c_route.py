#!/usr/bin/python3

"""This Script starts a flask web application:\
listening to port 5000 with routes:\
/ display "Hello HBNB", /hbnb: display "HBNB", :\
        /c/<text>: display “C ” followed by the:\
        value of the text variable """
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


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "C " + text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
