#!/usr/bin/python3
"""New view for City objs that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
        )
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    places_list = []
    cities = storage.get(City, city_id)
    if cities:
        for place in cities.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>', methods=['GET'], strict_slashes=False
        )
def get_place_by_id(place_id):
    """Retrieves a Place object by place id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_place_by_id(place_id):
    """Deletes a Place object by place id"""
    del_place = storage.get(Place, place_id)
    if del_place:
        storage.delete(del_place)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'],
        strict_slashes=False
        )
def create_place(city_id):
    """Creates a City object using the POST method"""
    city = storage.get(City, city_id)
    if city:
        content = request.get_json()

        # if body request is not a valid JSON, raise a 400 error with
        # response
        if type(content) is not dict:
            # if dict does not contain key=name, raise a 400 error with
            # response
            abort(400, description='Not a JSON')
        if 'user_id' not in content.keys():
            abort(400, description='Missing user_id')
        if 'name' not in content.keys():
            abort(400, description='Missing name')
        user = storage.get(User, content.get("user_id"))
        if not user:
            abort(404)
        # attempt to return new User with status code 201
        place = Place(**content)
        setattr(place, 'city_id', city_id)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False
        )
def update_place(place_id):
    """Updates a City object by given city_id"""
    place = storage.get(Place, place_id)
    if place:
        content = request.get_json()
        if type(content) is not dict:
            abort(400, description='Not a JSON')

        ignore_keys = [
            'id', 'user_id', 'city_id', 'created_at', 'updated_at'
            ]
        for key, val in content.items():
            if key not in ignore_keys:
                setattr(place, key, val)
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
