#!/usr/bin/python3
"""Starts a Flask web application"""
from models import storage
from flask import Flask as fl
from flask import render_template as rentem

app = fl(__name__)


@app.route("/states_list", strict_slashes=False)
def stateList():
    """Builds a list an ordered states list"""
    edit = "7-states_list.html"
    states = storage.all("State")
    return rentem(edit, states=states)


@app.teardown_appcontext
def SessTerm(exc):
    """Saves list and closes session to free resources"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
