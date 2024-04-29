#!/usr/bin/python3
"""New view for Review objs that handles all default RESTFul API
actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'],
        strict_slashes=False
        )
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a place"""
    reviews_list = []
    places = storage.get(Place, place_id)
    if places:
        for review in places.reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'], strict_slashes=False
        )
def get_review_by_id(review_id):
    """Retrieves a Review object by review id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_review_by_id(review_id):
    """Deletes a Review object by review id"""
    del_review = storage.get(Review, review_id)
    if del_review:
        storage.delete(del_review)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'],
        strict_slashes=False
        )
def create_review(place_id):
    """Creates a Review object using the POST method"""
    place = storage.get(Place, place_id)
    if place:
        content = request.get_json()
        # if body request is not a valid JSON, raise a 400 error with
        # response
        if type(content) is not dict:
            abort(400, description='Not a JSON')
        if 'user_id' not in content.keys():
            abort(400, description='Missing user_id')
        user = storage.get(User, content.get("user_id"))
        if not user:
            abort(404)
        if 'text' not in content.keys():
            abort(400, description='Missing text')
        # attempt to return new Review with status code 201
        review = Review(**content)
        setattr(review, 'place_id', place_id)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    else:
        abort(404)


@app_views.route(
        '/reviews/<review_id>', methods=['PUT'], strict_slashes=False
        )
def update_review(review_id):
    """Updates a City object by given place_id"""
    review = storage.get(Review, review_id)
    if review:
        content = request.get_json()
        if type(content) is not dict:
            abort(400, description='Not a JSON')

        ignore_keys = [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
            ]
        for key, val in content.items():
            if key not in ignore_keys:
                setattr(review, key, val)
        storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
