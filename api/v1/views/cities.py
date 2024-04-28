#!/usr/bin/python3
"""New view for State objs that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models import storage


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
        )
def get_cities(state_id):
    """Retrieves the list of all City objects"""
    cities_list = []
    states = storage.get('State', state_id)
    if states:
        for city in states.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>', methods=['GET'], strict_slashes=False
        )
def get_city_by_id(city_id):
    """Retrieves a City object by city id"""
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_city_by_id(city_id):
    """Deletes a City object by city id"""
    del_city = storage.get('City', city_id)
    if del_city:
        storage.delete(del_city)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'],
        strict_slashes=False
        )
def create_city(state_id):
    """Creates a State object using the POST method"""
    state = storage.get('State', state_id)
    if state:
        content = request.get_json()

        # if body request is not a valid JSON, raise a 400 error with response
        if type(content) is dict:
            # if dict does not contain key=name, raise a 400 error with response
            if 'name' in content.keys():
                # attempt to return new State with status code 201
                state = City(**content)
                storage.new(state)
                storage.save()
                return jsonify(state.to_dict()), 201
            else:
                response = jsonify({'error': 'Missing name'})
                response.status_code = 400
                return response
        else:
            response = jsonify({'error': 'Not a JSON'})
            response.status_code = 400
            return response
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>', methods=['PUT'], strict_slashes=False
        )
def update_city(city_id):
    """Updates a State object by given state_id"""
    city = storage.get(City, city_id)
    if city:
        content = request.get_json()
        if type(content) is not dict:
            response = jsonify({'error': 'Not a JSON'})
            response.status_code = 400
            return response

        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore_keys:
                setattr(city, key, val)
        storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
