#!/usr/bin/python3
"""__init__ - initializes the Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def display_cities_by_states():
    """Displays a list of states and their cities"""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states_sorted)


@app.teardown_appcontext
def teardown(exception):
    """Closes the SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

