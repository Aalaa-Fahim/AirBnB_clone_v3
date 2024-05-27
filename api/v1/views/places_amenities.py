#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")

@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        description: ID of the Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = [
            storage.get(Amenity, amenity_id)
            for amenity_id in place.amenity_ids
        ]
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        description: ID of the Place
      - name: amenity_id
        in: path
        type: string
        required: true
        description: ID of the Amenity
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.
    ---
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        description: ID of the Place
      - name: amenity_id
        in: path
        type: string
        required: true
        description: ID of the Amenity
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
