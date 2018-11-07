# Controller / Remote for controlling GPIO max_devices

import requests as r
import json as j
from time import sleep as s
from pathlib import Path
import os

def uin(msg):
    s(1)
    return input("(CTRL+C TO QUIT) *" + msg + "* - >> ")

config = j.load(open("config.json"))

server = config['server_address']

if server == "":
    print('''As you haven't specified an address in the config file,
    please enter the server address.\n
     EG: http://example.com:5252 OR http://10.0.0.1:1234''')

    server = uin("Input Server Address")

def MainMenu():
    print("Would you like to create a file, or execute an existing script?")
    option = uin("(N)ew | (E)xisting")
    option = option.lower()
    if option == "n":
        while True:
            print("Please select a name for the new script.")
            name = uin("Enter a name, or go (B)ack")
            if name.lower == "b":
                MainMenu()
                return
            elif os.path.isfile("data/" + name + ".ctrl"):
                print("A script with that name already exists. Try again.")

            else:
                CreateNewScript(name + ".ctrl")



    elif option == "e":
        # Get all files with extension ".ctrl"
        all_files = os.listdir("data")
        ctrl_files = []
        for fn in all_files:
            if fn.endswith(".ctrl"):
                ctrl_files.append(fn.replace(".ctrl", ""))


        if len(ctrl_files) <= 0:
            print("There seems to be no control / script files. Please import some, or create one.")
            uin("(ENTER / RETURN) for Main Menu")
            MainMenu()
            return

        else:
            print("The following control / script files are available:")
            s(1)
            print("=====[ID]==============[NAME]==============")
            for file in ctrl_files:
                print("\n      " + str(ctrl_files.index(file)) + "         " + file)

            print("Please choose from the following IDs, press enter for next page, or type 'M' for main menu.")
            option = uin("Enter ID, or (M)ain Menu")
            option = option.lower()
            if option == "m":
                MainMenu()
                return

            else:
                if option.isdigit():
                    index = int(option)
                    file = ctrl_files[index] + ".ctrl"
                    while True:
                        ExecuteExistingScript(file)
                        verdict = uin("(Return) Run script again, or (B)ack")
                        if verdict.lower == "b":
                            MainMenu()
                            return

                        else:
                            ExecuteExistingScript(file)

                    return

def ExecuteExistingScript(file):
    action = j.load(open("data/" + file))
    print("Executing action " + action['title'] + " with " + str(len(action['instructions'])) + " instructions, on stream " + action['stream'])
    resp = r.post(server + "/controller/create_action", json=action)
    if resp.status_code != 200:
        print("Something went wrong. Error code: " + str(resp.status_code))

    else:
        print("Successfully executed script on all subscribed devices.")

def CreateNewScript(file):
    print("EW")

MainMenu()
