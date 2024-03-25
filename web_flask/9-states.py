#!/usr/bin/python3
"""Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from models import storage
from flask import Flask as fl
from flask import render_template as rentem
from operator import itemgetter

app = fl(__name__)


@app.route("/states/<id>", strict_slashes=False)
def cityList(id):
    """Displays an HTML page with a list of all Cities with the id in the URL
    """
    states = storage.all("State").values()
    cities = storage.all("City").values()
    ret = None
    ctyList = []
    for elem in states:
        if elem.id == id:
            ret = elem.name
    for elem in cities:
        if elem.state_id == id:
            ctyList.append([elem.id, elem.name])
    ctyList = sorted(ctyList, key=itemgetter(1))
    return rentem("9-states.html", statName=ret, statctys=ctyList)


@app.route("/states", strict_slashes=False)
def stateList():
    """Displays an HTML page with a list of all State objects in DBStorage.
    States are sorted by name.
    """
    states = storage.all("State")
    temp = states.values()
    return rentem("9-states.html", listed=temp)


@app.teardown_appcontext
def sessClos(arg=None):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
