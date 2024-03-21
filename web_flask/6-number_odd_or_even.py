#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask as fl
from flask import render_template as rentem

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
def pythonGame(text="is cool"):
    """
    A small game of adding the most child route to a sentance and displaying it
    """
    temp = text.replace("_", " ")
    return "Python {}".format(temp)


@app.route("/number/<int:n>", strict_slashes=False)
def numberGame(n):
    """
    A small game of adding the most child route to a sentance and displaying it
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def numberTemplate(n):
    """Builds a page to displays the passed number in"""
    return rentem("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
