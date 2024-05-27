#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
        description: ID of the City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
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
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object.
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
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object.
    ---
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
        description: ID of the City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        abort(400, description="Missing user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
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
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
