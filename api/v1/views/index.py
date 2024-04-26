#!/usr/bin/python3
"""
index module for API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


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
    classes = [
        "Amenity",
        "City",
        "Place",
        "Review",
        "State",
        "User"]
    json_return = {}
    for classs in classes:
        item_count = storage.count(eval(classs))
        json_return[classs] = item_count
    return jsonify(json_return)
