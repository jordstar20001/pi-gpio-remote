# Server program. Jordan Zdimirovic (C)

from flask import Flask, request, make_response, jsonify

import requests as reqs
import json
import os
import codecs

# Get config from config.json

config = {}

with open('config.json') as f:
    config = json.load(f)

server = Flask(__name__)

# Runtime vars ------

subscribers = {}

@server.route("/new_subscription", methods="POST")
def new_subscription():
    sub_id = str(codecs.encode(os.urandom(16), 'hex').decode())
    data = request.jsonify()
    subscribers[sub_id] = {
        ""
    }
