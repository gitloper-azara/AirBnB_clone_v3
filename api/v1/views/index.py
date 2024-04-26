#!/usr/bin/python3
"""
index module for API
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def return_status():
    """returns a json of route status"""
    status = {
        "status": "OK"
    }
    return jsonify(status)
