#!/usr/bin/python3
""" script that starts a Flask web application :\
        which will be  listening on 0.0.0.0, port 5000:\
        with routes /: display “Hello HBNB!”:\
        /hbnb: display “HBNB” :\
        /c/<text>: display “C ”, followed by the value :\
        of the text variable /python/<text>displaying “Python ”, :\
        followed by the value of the text variable"""

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


""" Define a route that takes a text variable :\
        and displays "C " followed by the value """


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "C " + text


"""  Define a route that takes a text variable and displays:\
        "Python " followed by the value"""
# If no text is provided, use the default value "is cool"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "Python " + text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
