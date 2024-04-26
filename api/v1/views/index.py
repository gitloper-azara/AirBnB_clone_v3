#!/usr/bin/python3
"""
index module for API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def return_status():
    """returns a json of route status"""
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route('/stats')
def num_obj_by_type():
    """returns the number of each obj by type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    json_return = {}
    for key, val in classes.items():
        item_count = storage.count(eval(val))
        json_return[key] = item_count
    return jsonify(json_return)
