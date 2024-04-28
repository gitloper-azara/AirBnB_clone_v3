#!/usr/bin/python3
"""New view for Amenity objs that handles all default RESTFul API
actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route(
        '/amenities', methods=['GET'], strict_slashes=False
        )
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_list = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False
        )
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by amenity id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False
        )
def delete_amenity_by_id(amenity_id):
    """Deletes a City object by amenity id"""
    del_amenity = storage.get(Amenity, amenity_id)
    if del_amenity:
        storage.delete(del_amenity)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route(
        '/amenities', methods=['POST'], strict_slashes=False
        )
def create_amenity():
    """Creates a State object using the POST method"""
    content = request.get_json()

    # if body request is not a valid JSON, raise a 400 error with
    # response
    if type(content) is dict:
        # if dict does not contain key=name, raise a 400 error with
        # response
        if 'name' in content.keys():
            # attempt to return new State with status code 201
            amenity = Amenity(**content)
            storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            return abort(400, description='Missing name')
    else:
        return abort(400, description='Not a JSON')


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False
        )
def update_amenity(amenity_id):
    """Updates an Amenity object by given amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        content = request.get_json()
        if type(content) is not dict:
            return abort(400, description='Not a JSON')

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore_keys:
                setattr(amenity, key, val)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
