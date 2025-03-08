#!/usr/bin/python3
"""__init__ - initializes the Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display_states():
    """Displays a list of all State objects"""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('9-states.html', states=states_sorted)


@app.route('/states/<state_id>', strict_slashes=False)
def display_cities_by_state(state_id):
    """Displays cities of a specific State"""
    state = storage.get(State, state_id)
    if state:
        return render_template('9-states.html', state=state)
    return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown(exception):
    """Closes the SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

