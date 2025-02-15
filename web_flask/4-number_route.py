#!/usr/bin/python3
"""A simple Flask web application."""
from flask import Flask

# Initialize the Flask application
app = Flask(__name__)
# Disable strict trailing slashes rule
app.url_map.strict_slashes = False

@app.route('/')
def index():
    """Route for the home page."""
    return 'Hello HBNB!'

@app.route('/hbnb')
def hbnb():
    """Route for the HBNB page."""
    return 'HBNB'

@app.route('/c/<text>')
def c_page(text):
    """Route for the C page with dynamic text.
    
    Args:
        text (str): The dynamic part of the URL.

    Returns:
        str: Formatted string with 'C' followed by the provided text.
    """
    return 'C {}'.format(text.replace('_', ' '))

@app.route('/python/<text>')
@app.route('/python', defaults={'text': 'is cool'})
def python_page(text):
    """Route for the Python page with dynamic text.
    
    Args:
        text (str): The dynamic part of the URL. Defaults to 'is cool'.

    Returns:
        str: Formatted string with 'Python' followed by the provided text.
    """
    return 'Python {}'.format(text.replace('_', ' '))

@app.route('/number/<int:n>')
def number_page(n):
    """Route for the number page with dynamic integer.
    
    Args:
        n (int): The integer provided in the URL.

    Returns:
        str: Formatted string indicating the provided number.
    """
    return '{} is a number'.format(n)

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
