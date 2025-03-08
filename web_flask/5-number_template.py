#!/usr/bin/python3
""" Script that starts a flask web application:\
        listening to port 5000:\
        routes
        /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ”, followed by the value :\
            of the text variable.
    /python/(<text>): display “Python ”, :\
            followed by the value of the text variable
        The default value of text is “is cool”:\
                /number/<n>: display “n is a number” only if n is an integer:\
                /number_template/<n>: display a HTML page:\
                only if n is an integer:
        H1 tag: “Number: n” inside the tag BODY """
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

# Define a route that takes a text variable and displays:\
# "C " followed by the value


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "C " + text

# Define a route that takes a text variable:\
# and displays "Python " followed by the value
# If no text is provided, use the default value "is cool"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    text = text.replace('_', ' ')  # Replace underscores with spaces
    return "Python " + text

# Define a route that takes an integer:\
# and displays a template if n is an integer


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
