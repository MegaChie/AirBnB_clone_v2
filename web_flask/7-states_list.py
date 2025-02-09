#!/usr/bin/python3
"""
   simple flask app

"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def  html_page_3():
    """ fetching data """
    states = sorted( list(storage.all("State").values()), lambda: x: x.name)
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def close_storage(exception):
    """ remove current SQLAlchemy session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
