#!/usr/bin/python3
"""
New view for the link between Place objs and Amenity objs that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models.place import Place
from models.amenity import Amenity
from models import storage
from models import storage_t


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'],
        strict_slashes=False
        )
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a place"""
    amenities_list = []
    places = storage.get(Place, place_id)
    if places:
        if storage_t == 'db':
            for amenity in places.amenities:
                amenities_list.append(amenity.to_dict())
        else:
            amenities_list = []
            for amenity_id in places.amenity_id:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False
        )
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    del_amenity = storage.get(Amenity, amenity_id)
    if not del_amenity:
        abort(404)

    if storage_t == 'db':
        if del_amenity not in place.amenities:
            abort(404)
        storage.delete(del_amenity)
        storage.save()
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        storage.delete(amenity_id)
        storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
        strict_slashes=False
        )
def link_amenity_place(place_id, amenity_id):
    """Link an Amenity object to a place using the POST method"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            storage.save()
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity)
            storage.save()
    return jsonify(amenity.to_dict()), 201
