# Device Program, Jordan Zdimirovic (C)
# This program is for the device Raspberry Pi 3 Model B
from flask import Flask, request, make_response, jsonify

import requests as reqs
import json

import gpiozero as pio

# Get config from config.json

config = {}

with open('config.json') as f:
    config = json.load(f)

streams = config['streams']

server_address = config['server_address']

dev_port = config['this_port']

device_name = config['name']

# Subscribe to the server.

reqs.post(server_address + "/new_subscription", {
    "device_name":device_name,
    ""
})

device = Flask(__name__)

# RUNTIME VARS -----

subs = streams

@device.route("/heartbeat", methods=["GET"])
def heartbeat():
    return make_response(), 200

@device.route("/new_instructions", methods=["POST"])
def instructions_received():
    data = request.get_json()
    if data.stream not in subs:
        return make_response(), 400


    else:
        print("Performing " + data['title'] + " from " + data['stream'])
        instructions = data['instructions']
        for i in range(0, data['loops'] - 1):
            for instruct in instructions:
                pin = instruct['pin']
                component = instruct['component_type']
                action = instruct['action']
                delay = instruct['delay']
                if component == "led":
                    light = pio.LED(pin)
                    if action == "ON":
                        light.on()

                    elif action == "OFF":
                        light.off()

                    elif action == "TOGGLE":
                        light.toggle()

                elif component == "variled":
                    light = pio.PWMLED(pin)
                    if action == "SET":
                        light.value = instruct['value']

                elif component == "buzzer":
                    bz = pio.Buzzer(pin)
                    if action == "ON":
                        bz.on()

                    elif action == "OFF":
                        bz.off()

                    elif action == "TOGGLE":
                        bz.toggle()

                elif component == "servo":
                    servo = pio.Servo(pin)
                    if action == "MIN":
                        servo.min()

                    elif action == "MAX":
                        servo.max()

                    elif action == "MID":
                        servo.mid()


device.listen("0.0.0.0", dev_port)
