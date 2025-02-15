#!/usr/bin/python3
"""
A simple Flask web application.
"""
from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Disable strict slashes for the URL map
app.url_map.strict_slashes = False

@app.route('/')
def index():
    """
    The home page route.
    Returns a greeting message.
    """
    return 'Hello HBNB!'

if __name__ == '__main__':
    # Run the Flask application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port='5000')
