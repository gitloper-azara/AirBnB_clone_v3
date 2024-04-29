#!/usr/bin/python3
"""New view for User objs that handles all default RESTFul API
actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route(
        '/users', methods=['GET'], strict_slashes=False
        )
def get_users():
    """Retrieves the list of all User objects"""
    user_list = []
    users = storage.all(User)
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route(
        '/users/<user_id>', methods=['GET'], strict_slashes=False
        )
def get_user_by_id(user_id):
    """Retrieves a User object by user id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route(
        '/users/<user_id>', methods=['DELETE'],
        strict_slashes=False
        )
def delete_user_by_id(user_id):
    """Deletes a User object by user_id"""
    del_user = storage.get(User, user_id)
    if del_user:
        storage.delete(del_user)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route(
        '/users', methods=['POST'], strict_slashes=False
        )
def create_user():
    """Creates a User object using the POST method"""
    content = request.get_json()

    # if body request is not a valid JSON, raise a 400 error with
    # response
    if type(content) is dict:
        # if dict does not contain key=name, raise a 400 error with
        # response
        if 'email' not in content.keys():
            return abort(400, description='Missing email')
        if 'password' not in content.keys():
            return abort(400, description='Missing password')
        # attempt to return new State with status code 201
        user = User(**content)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    else:
        return abort(400, description='Not a JSON')


@app_views.route(
        '/users/<user_id>', methods=['PUT'], strict_slashes=False
        )
def update_user(user_id):
    """Updates an User object by given user_id"""
    user = storage.get(User, user_id)
    if user:
        content = request.get_json()
        if type(content) is not dict:
            return abort(400, description='Not a JSON')

        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore_keys:
                setattr(user, key, val)
        storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
