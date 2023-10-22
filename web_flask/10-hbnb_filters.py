#!/usr/bin/python3
""" Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def state_id():
    """ Display HBNB filters page """
    return render_template(
        '10-hbnb_filters.html',
        states=storage.all(State), amenities=storage.all(Amenity))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
