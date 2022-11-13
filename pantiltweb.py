#!/usr/bin/env python

import pantilthat
import colorsys
import math
import time

from sys import exit


try:
    from flask import Flask, render_template
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

app = Flask(__name__)

pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)


@app.route('/')
def home():
    return render_template('gui.html')

@app.route('/api/<direction>/<int:angle>')
def api(direction, angle):
    if angle < 0 or angle > 180:
        return "{'error':'out of range'}"

    angle -= 90

    if direction == 'pan':
        pantilthat.pan(angle)
        return "{{'pan':{}}}".format(angle)

    elif direction == 'tilt':
        pantilthat.tilt(angle)
        return "{{'tilt':{}}}".format(angle)

    return "{'error':'invalid direction'}"

@app.route('/light/<lightOn>/<int:r>/<int:g>/<int:b>')
def light(lightOn, r, g, b):
    if lightOn == 'on':
        pantilthat.set_all(r, g, b)
        pantilthat.show()
        return "{'light':'changed'}"

    pantilthat.set_all(0, 0, 0)
    pantilthat.show()
    return "{'light':'off'}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9595, debug=True)

