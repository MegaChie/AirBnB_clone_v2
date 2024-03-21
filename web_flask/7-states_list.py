#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask as fl
from flask import render_template as rentem
from models import storage

app = fl(__name__)


@app.route("/states_list", strict_slashes=False)
def stateList():
    """Builds a list an ordered states list"""
    path = "7-states_list.html"
    states = storage.all(State)
    return rentem(path, states=states)


@app.teardown_appcontext
def SessTerm(arg=None):
    """Saves list and closes session to free resources"""
    storage.close()


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
