#!/usr/bin/python3
"""
Starts a Flask web application.
The application should listens on 0.0.0.0, port 5000.
"""
from flask import Flask
from models import storage
from flask import render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states()
    """ To Displays 'Hello HBNB!'."""
    states = storage.all("State")
    return render_template("9-states.html", state=states)

@app.route("/hbnb", strict_slashes=False)
def states_id(id):
    """ To Displays 'HBNB'."""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
