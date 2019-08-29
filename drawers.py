from flask import Flask, render_template, request
from flask_cors import CORS
import time
import random
import json
import RPi.GPIO as GPIO
import sys
print(sys.path)
app = Flask(__name__)
CORS(app)

GPIO.setmode(GPIO.BCM)

pins = {
    1: {'name': 'GPIO 1', 'state': GPIO.LOW},
    2: {'name': 'GPIO 2', 'state': GPIO.LOW},
    3: {'name': 'GPIO 3', 'state': GPIO.LOW},
    4: {'name': 'GPIO 4', 'state': GPIO.LOW},
    5: {'name': 'GPIO 5', 'state': GPIO.LOW},
    6: {'name': 'GPIO 6', 'state': GPIO.LOW},
    7: {'name': 'GPIO 7', 'state': GPIO.LOW},
    #    8: {'name': 'GPIO 8', 'state': GPIO.LOW},
    #    9: {'name': 'GPIO 9', 'state': GPIO.LOW},
    #    10: {'name': 'GPIO 10', 'state': GPIO.LOW}
}

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def switchPin(pin, state):
    print(pin, state)
    if state == "on":
        signal = GPIO.HIGH
    else:
        signal = GPIO.LOW
    GPIO.output(pin, signal)


def readPins():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)


def dance(duration):
    loopNumber = int(duration/0.2)
    for loop in range(loopNumber):
        allOn()
        randomPin = random.choice(list(pins))
        switchPin(randomPin, 'off')
        time.sleep(0.2)
    allOff()


def allOn():
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)


def allOff():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    dance(5)
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # If the action part of the URL is "on," execute the code indented below:
    switchPin(changePin, action)
    # For each pin, read the pin state and store it in the pins dictionary:
    readPins()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# Reset all pins
@app.route("/reset")
def reset():
    allOff()
    readPins()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
