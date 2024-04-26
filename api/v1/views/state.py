#!/usr/bin/python3
"""New view for State objs that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states_list = []
    states = storage.all('State')
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)
