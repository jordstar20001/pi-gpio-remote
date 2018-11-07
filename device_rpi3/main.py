# Device Program, Jordan Zdimirovic (C)
# This program is for the device Raspberry Pi 3 Model B
from flask import Flask, request, make_response, jsonify

import requests as reqs
import json

import time

import gpiozero as pio

device_identifier = ""

# Get config from config.json

config = {}

with open('config.json') as f:
    config = json.load(f)

streams = config['streams']

server_address = config['server_address']

device_port = config['this_port']

device_name = config['name']

device_ip = config['this_ip']

max_connect_attempts = config['max_connect_attempts']

# Subscribe to the server.
connectionAttempts = 0
def ConnectToServer():
    global connectionAttempts
    global device_identifier
    dev_add = device_ip + ":" + str(device_port)
    print("!!!! " + dev_add + " : " + str(type(dev_add)))
    resp = reqs.post(server_address + "/new_device", json= {"device_ip":dev_add,"device_name":device_name})

    if resp.status_code == 200:
        device_identifier = resp.json()['id']

    else:
        connectionAttempts += 1
        if connectionAttempts >= max_connect_attempts:
            print("Error. Failed to connect after " + str(max_connect_attempts) + " attempts. Ending session in 5 seconds...")
            time.sleep(5)
            quit()

        else:
            print("Error. Failed to connect to server. Trying again in 3 seconds.")
            time.sleep(3)
            ConnectToServer()

ConnectToServer()

at_least_one_stream_hosted = False
subs = []
for stream in streams:
    req = reqs.post(server_address + "/new_subscription", json={
        "stream":stream,
        "id":device_identifier
    })
    if req.status_code != 200:
        if at_least_one_stream_hosted or (len(streams) - 1) != streams.index(stream):
            print("Error. The stream is not being hosted by the server. Trying next stream...")

        else:
            print("Error. None of the streams are hosted on the server. Ending session in 5 seconds...")
            time.sleep(5)
            quit()

    else:
        subs.append(stream)
        at_least_one_stream_hosted = True

device = Flask(__name__)

# RUNTIME VARS -----



@device.route("/heartbeat", methods=["GET"])
def heartbeat():
    return make_response(jsonify(config)), 200

@device.route("/new_instructions", methods=["POST"])
def instructions_received():
    data = request.get_json()
    if data['stream'] not in subs:
        return make_response(), 400


    else:
        try:
            print("Performing " + data['title'] + " from " + data['stream'])
            #instructions = data['instructions']
            print("LOOOOOOOOOOOOOOOOOOP : " + data["loops"])

            for i in range(0, data['loops'] - 1):
                print("LOOP #" + str(i))
                for instruct in instructions:
                    pin = instruct['pin']
                    component = instruct['component_type']
                    action = instruct['action']
                    delay = instruct['delay']
                    if component == "led":
                        print("LED!!!!!!!!!!!!!!!!")
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

                    time.sleep(delay / 1000)

            return make_response(), 200
        except Exception as e:
            print("Ooooops! Something went wrong... " + e)
            return make_response(), 402
device.run("0.0.0.0", device_port)
