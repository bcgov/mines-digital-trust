#!/usr/bin/env python
from flask import Flask, jsonify, abort, request, make_response

import requests
import json
import os
import yaml

import signal

from app import config, issuer,routes

class Controller(Flask):
    def __init__(self, ENV):
        print("Initializing " + __name__ + " ...")
        super().__init__(__name__)
        issuer.startup_init(ENV)
        self.ENV = ENV


def create_app(ENV):
    app = Controller(ENV)
    routes.register_routes(app)
    wsgi_app = app.wsgi_app
    return app

signal.signal(signal.SIGINT, issuer.signal_issuer_shutdown)
signal.signal(signal.SIGTERM, issuer.signal_issuer_shutdown)


# Load application settings (environment)
config_root = os.environ.get('CONFIG_ROOT', './config')
ENV = config.load_settings(config_root=config_root)
app = create_app(ENV)
