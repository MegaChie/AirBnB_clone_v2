#!/usr/bin/python3
""" A script that starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_states():
    """
    Renders states_list htmf to display states created.
    """
    path = '7-states_list.html'
    states = storage.all(State)
    s = sorted(states.values(), key=lambda state: state.name)
    return render_template(path, s=s)


@app.teardown_appcontext
def teardown(exception_object):
    """
    Used for cleaning up resources or performing actions after
    a request has been processed.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
