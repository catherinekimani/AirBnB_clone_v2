#!/usr/bin/python3
""" Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    """ Html page with a list of states and cities """
    return render_template(
        '8-cities_by_states.html', states=storage.all(State))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
