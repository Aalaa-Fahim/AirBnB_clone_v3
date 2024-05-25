#!/usr/bin/python3
"""Sttus of our app"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status_of_api():
    """to check status"""
    response = {'status': 'OK'}
    return (jsonify(response))


@app_views.route("/stats")
def stats():
    """endpoint that retrieves the number of each objects by type"""
    stats = {
            "states": storage.count('State'),
            "cities": storage.count('City'),
            "amenities": storage.count('Amenity'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "users": storage.count('User')
            }
    return (jsonify(stats))
