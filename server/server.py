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

streams_available = config['streams']

listen_port = config['port']

server = Flask(__name__)

# Runtime vars ------

subscribers = {}

@server.route("/new_device", methods=["POST"])
def new_device():
    device_id = str(codecs.encode(os.urandom(16), 'hex').decode())
    data = request.get_json()
    print(data)
    print(data['device_ip'])
    print(data['device_name'])
    subscribers[device_id] = {
        "device_ip":data["device_ip"],
        "device_name":data["device_name"],
        "streams":[]
    }
    return make_response(jsonify({
        "id":device_id
    })), 200

@server.route("/new_subscription", methods=["POST"])
def new_subscription():
    data = request.get_json()
    device_id = data['id']
    stream = data['stream']
    if stream in streams_available:
        subscribers[device_id][streams].append(stream)
        return make_response(), 200

    else:
        return make_response(), 400


@server.route("/get_streams", methods=["GET"])
def get_streams():
    return make_response(jsonify({
        "streams":streams_available
    })), 200

@server.route("/controller/create_action", methods=["POST"])
def send_action_to_devices():
    r_data = request.get_json()
    stream = r_data["stream"]
    title = r_data["title"]
    if stream not in streams_available:
        return make_response(), 404

    for device in subscribers:
        if stream in device[streams]:
            # Send instructions to the device
            device_address = device["device_ip"]
            device_name = device["device_name"]
            print("Sending " + title + " from stream " + stream + " to device " + device_name + " at IP: " + device_address + "...")
            reqs.post(device_address + "/new_instructions", data=data)




server.run("0.0.0.0", listen_port)
