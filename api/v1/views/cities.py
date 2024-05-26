#!/usr/bin/python3
"""
create a new view for City objects that handles all default
RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves all City objects of a State
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object by its id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    for key, value in city_json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict())