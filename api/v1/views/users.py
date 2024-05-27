#!/usr/bin/python3
"""
Route for handling User objects and operations
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.
    ---
    responses:
      200:
        description: List of User objects
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object.
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID of the User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object.
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID of the User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """
    Creates a User object.
    """
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object.
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: ID of the User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
