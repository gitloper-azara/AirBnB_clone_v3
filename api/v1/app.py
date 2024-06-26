#!/usr/bin/python3
"""
starts API
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


# create a variable app, instance of Flask
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(exception):
    """Closes db"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """custom 404 display using json"""
    err_message = {
        "error": "Not found"
    }
    return jsonify(err_message), 404


if __name__ == '__main__':
    # get host and port from environment variables or use default
    # if not environment variables
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # run Flask server
    app.run(host=host, port=port, threaded=True)
