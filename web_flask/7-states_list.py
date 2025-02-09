#!/usr/bin/python3
"""
   simple flask app

"""

from flask import Flask, render_template
from models import storage
from models import *

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def  html_page_3():
    """ fetching data """
    states = list(storage.all("State").values())
    sorted_states = sorted(states, key=lambda: x: x.name)
    return render_template('7-states_list.html', states=sorted_states)

@app.teardown_appcontext
def close_storage(exception):
    """ remove currnet SQLAlchemy session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
