#!/usr/bin/python3
"""New view for State objs that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
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


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a State object by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_obj = state.to_dict()
    return jsonify(state_obj)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes a State object by id"""
    if state_id:
        del_state = storage.get(State, state_id)
        if not del_state:
            abort(404)
        del_state.delete()
        storage.save()
        storage.close()
        return jsonify({}), 200
