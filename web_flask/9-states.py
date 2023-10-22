#!/usr/bin/python3
""" Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """ Display html page with a list of states and cities """
    return render_template('7-states_list.html', states=storage.all(State))


@app.route("/states/<string:id>", strict_slashes=False)
def states_id(id=None):
    """ display html page with info about <id> """
    return render_template(
        '9-states.html', states=storage.all(State).get('State.{}'.format(id)))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
