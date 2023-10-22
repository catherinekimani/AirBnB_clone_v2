#!/usr/bin/python3
""" Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


def cities_by_state():
    """ Html page with a list of states and cities """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
