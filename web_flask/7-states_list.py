#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask as fl
from flask import render_template as rentem
from models import storage
from models.state import State

app = fl(__name__)


@app.route("/states_list")
def stateList():
    """Builds a list an ordered states list"""
    path = "7-states_list.html"
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return rentem(path, sorted_states=sorted_states)


@app.teardown_appcontext
def SessTerm(arg=None):
    """Saves list and closes session to free resources"""
    storage.close()


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000)
