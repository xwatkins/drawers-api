import RPi.GPIO as GPIO
from flask import Flask, jsonify
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
    23: {'name': 'GPIO 23', 'state': GPIO.LOW},
    24: {'name': 'GPIO 24', 'state': GPIO.LOW}
}

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        GPIO.output(changePin, GPIO.HIGH)
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
    return 'OK'

# Reset all pins
@app.route("/reset")
def reset():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
