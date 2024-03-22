#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask as fl

app = fl(__name__)


@app.route("/", strict_slashes=False)
def greeting():
    """Greets the user with a welcoming message"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNBGreeting():
    """Returns a message on the hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def cGame(text):
    """
    A small game of adding the most child route to a sentance and displaying it
    """
    temp = text.replace("_", " ")
    return "C {}".format(temp)


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def pythonGame(text="is cool"):
    """
    A small game of adding the most child route to a sentance and displaying it
    """
    temp = text.replace("_", " ")
    return "Python {}".format(temp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
