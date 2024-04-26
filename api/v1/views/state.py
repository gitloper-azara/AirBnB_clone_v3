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


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a State object using the POST method"""
    content = request.get_json()

    # if body request is not a valid JSON, raise a 400 error with response
    if not content:
        abort(400, 'Not a JSON')
    # if dict does not contain key=name, raise a 400 error with response
    if 'name' not in content:
        abort(400, 'Missing name')

    # attempt to return new State with status code 201
    state = State(**content)
    storage.new(state)
    state.save()
    storage.close()

    state_obj = state.to_dict()
    return jsonify(state_obj), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object by given state_id"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    content = request.get_json()
    if not content:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in ignore_keys:
            setattr(states, key, val)
    states.save()
    storage.close()

    state_obj = states.to_dict()
    return jsonify(state_obj), 200
