#!/usr/bin/python3
"""
starts API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


# create a variable app, instance of Flask
app = Flask(__name__)
app.register_blueprint(app_views)


if __name__ == '__main__':
    # get host and port from environment variables or use default
    # if not environment variables
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # run Flask server
    app.run(host=host, port=port, threaded=True)
