#!/usr/bin/python3
"""To create Flask app """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_method(exception):
    """To call storage.close() to remove the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''to handel errors not found'''
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    ''' Main to run the Flask app'''
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
