#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import os
from time import sleep
import socket
import requests
import datetime

from smartFan import smartFan
from rgbStrip import rgbStrip
from smartLight import smartLight
from lightswitch import lightswitch
from smartThermostat import smartThermostat

app = Flask(__name__)

lightswitchIPs = ['192.168.11.11']
fanIPs = ['192.168.11.5','192.168.11.6', '192.168.11.7']
lightIPs = [] #['192.168.11.7'] 
rgbStripIP = '192.168.11.10'
thermostatIP = '192.168.11.13'

# initialize fans
smartFans = []
for fanIP in fanIPs:
    smartFans.append(smartFan(fanIP))

# init rgbStrip
rgbStrip1 = rgbStrip(rgbStripIP)

# initialize smart lights
smartLights = []
for lightIP in lightIPs:
    smartLights.append(smartLight(lightIP, offon=True))

# init lightswitches for old fashioned lights
lightswitches = []
for lightswitchIP in lightswitchIPs:
    lightswitches.append(lightswitch(lightswitchIP, inverted=True))

# init thermostat
thermostat = smartThermostat(thermostatIP)

# files
base = 'index.html'


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

"""
    Display home page
"""
@app.route("/")
def index():
    # make sure not getting any out of bounds errors
    fanOnColors = [""] * 3
    fanOffColors = [""] * 3
    for i in range(0, len(smartFans)):
        fanOnColors[i] = smartFans[i].getOnButtonColor()
        fanOffColors[i] = smartFans[i].getOffButtonColor()
    
    lightOnColors = [""] * 3
    lightOffColors = [""] * 3
    for i in range(0, len(smartLights)):
        lightOnColors[i] = smartLights[i].getOnButtonColor()
        lightOffColors[i] = smartLights[i].getOffButtonColor()

    lightswitchOnColors = [""] * 2
    lightswitchOffColors = [""] * 2
    for i in range(0, len(lightswitches)):
         lightswitchOnColors[i] = lightswitches[i].getOnButtonColor()    

    # things to return in template
    values = {
            "r" : rgbStrip1.getR(),
            "g" : rgbStrip1.getG(),
            "b" : rgbStrip1.getB(),
            "brightness" : rgbStrip1.getBrightness(),
            "color" : rgbStrip1.getHex(),
            "brightnessButton1BackgroundColor" : rgbStrip1.getBrightnessButtonColors()[0],
            "brightnessButton2BackgroundColor" : rgbStrip1.getBrightnessButtonColors()[1],
            "brightnessButton3BackgroundColor" : rgbStrip1.getBrightnessButtonColors()[2],
            "brightnessButton4BackgroundColor" : rgbStrip1.getBrightnessButtonColors()[3],
            "numFans" : len(smartFans),
            "fan1OnButtonBackgroundColor" : fanOnColors[0],
            "fan1OffButtonBackgroundColor" : fanOffColors[0],
            "fan2OnButtonBackgroundColor" : fanOnColors[1],
            "fan2OffButtonBackgroundColor" : fanOffColors[1],
            "fan3OnButtonBackgroundColor" : fanOnColors[2],
            "fan3OffButtonBackgroundColor" : fanOffColors[2],
            "numLights" : len(smartLights),
            "light1OnButtonBackgroundColor" : lightOnColors[0], 
            "light1OffButtonBackgroundColor" : lightOffColors[0],
            "light2OnButtonBackgroundColor" : lightOnColors[1], 
            "light2OffButtonBackgroundColor" : lightOffColors[1],
            "light3OnButtonBackgroundColor" : lightOnColors[2], 
            "light3OffButtonBackgroundColor" : lightOffColors[2],
            "numSwitches" : len(lightswitches),
            "ls1OnBgColor" : lightswitchOnColors[0],
            "ls1OffBgColor" : lightswitchOffColors[0], \
            "ls2OnBgColor" : lightswitchOnColors[1], 
            "ls2OffBgColor" : lightswitchOffColors[1], \
            "currentTemp" : thermostat.getTemp(), 
            "currentThreshold" : thermostat.getThreshold(), 
            "targetTemp" : thermostat.getTargetTemp()
            }

    return render_template(base, **values)
    
@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == password:
        session['logged_in'] = True
    else:
        flash('Wrong password!')
    return index()

# not included anywhere yet
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


"""
    RGB SUBSYSTEM
"""
@app.route("/sliders", methods=["POST"])
def sliders():
    # Get slider Values
    r = int(request.form["r"])
    g = int(request.form["g"])
    b = int(request.form["b"])

    rgbStrip1.setRGB(r, g, b)

    return index()

@app.route("/button", methods=["POST"])
def button():
    hexString = (request.form["button"])
    r,g,b = rgbStrip1.hextoRGB(hexString)
    rgbStrip1.setRGB(r, g, b)
    
    return index()

@app.route("/brightness", methods=["POST"])
def brightness():
    brightness = int(request.form["brightness"])
    rgbStrip1.setBrightness(brightness)
    
    return index()

@app.route("/effects", methods=["POST", "GET"])
def effects():
    if request.method == 'POST':
        selectedEffect = (request.form["effect"])
    else:
        selectedEffect = request.args.get("effect")
    
    rgbStrip1.setEffect(selectedEffect)

    return index()

"""
    Fans subsystem
"""
@app.route("/fans", methods=["POST", "GET"])
def fans():
    if request.method == "POST":
        status = request.form["fans"]
    else:
        status = request.args.get("fans")

    for fan in smartFans:
        #change status of fan
        fan.setStatus(status)

    return index()
    
@app.route("/fan1toggle", methods=["GET", "POST"])
def fan1toggle():
    smartFans[0].invertStatus()

    return index()

@app.route("/fan2toggle", methods=["POST"])
def fan2toggle():
    smartFans[1].invertStatus()

    return index()

@app.route("/fan3toggle", methods=["POST"])
def fan3toggle():
    smartFans[2].invertStatus()

    return index()

# bottom on/off switches
@app.route("/fan1", methods=["GET", "POST"])
def fan1():
    # get status
    if request.method == 'POST':
        status = request.form["fan"]
    else:
        status = request.args.get("fan")
    
    # update fan
    smartFans[0].setStatus(status)
    
    return index()

@app.route("/fan2", methods=["GET", "POST"])
def fan2():
    # get status
    if request.method == 'POST':
        status = request.form["fan"]
    else:
        status = request.args.get("fan")
    
    # update fan
    smartFans[1].setStatus(status)
   
    return index()

@app.route("/fan3", methods=["GET", "POST"])
def fan3():
    # get status
    if request.method == 'POST':
        status = request.form["fan"]
    else:
        status = request.args.get("fan")
    
    # update fan
    smartFans[2].setStatus(status)
    
    return index()

"""
    Light subsystem
"""
@app.route("/lights", methods=["POST"])
def lights():
    status = request.form["lights"]

    for light in smartLights:
        #change status of light
        light.setStatus(status)

    return index()
    
@app.route("/light1toggle", methods=["GET", "POST"])
def light1toggle():
    smartLights[0].invertStatus()

    return index()

@app.route("/light2toggle", methods=["POST"])
def light2toggle():
    smartLights[1].invertStatus()

    return index()

@app.route("/light3toggle", methods=["POST"])
def light3toggle():
    smartFans[2].invertStatus()

    return index()

# bottom on/off switches
@app.route("/light1", methods=["GET", "POST"])
def light1():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    # update light
    smartLights[0].setStatus(status)
    
    return index()

@app.route("/light2", methods=["GET", "POST"])
def light2():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    # update light
    smartLights[1].setStatus(status)
   
    return index()

@app.route("/light3", methods=["GET", "POST"])
def light3():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    # update light
    smartLights[2].setStatus(status)
    
    return index()

@app.route("/switches", methods=["GET", "POST"])
def switches():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    print(status)

    for switch in lightswitches:
        switch.setStatus(status)

    return index()

@app.route("/switch1", methods=["GET", "POST"])
def switch1():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    lightswitches[0].setStatus(status)

@app.route("/switch2", methods=["GET", "POST"])
def switch2():
    # get status
    if request.method == 'POST':
        status = request.form["light"]
    else:
        status = request.args.get("light")
    
    lightswitches[1].setStatus(status)

"""
    Record temperature
"""
@app.route("/temp", methods=["GET"])
def temp():
    print(request.method)
    temp1 = request.args.get("temp1")
    
    with open('temperatures.txt', 'a') as fh:
        appendStr = str(datetime.datetime.now()) + ", " + temp1 + "\n"
        fh.write(appendStr)

    return index()

"""
    Thermostat
"""
@app.route("/tempControl", methods=["POST"])
def tempControl():
    status = request.form["status"]
    thermostat.setStatus(status)
    return index()

@app.route("/setDesiredTemp", methods=["POST"])
def setDesiredTemp():
    desiredTemp = request.form["temp"]
    thermostat.setTemp(desiredTemp)
    return index()

@app.route("/setDesiredThreshold", methods=["POST"])
def setDesiredThreshold():
    desiredThreshhold = request.form["threshold"]
    thermostat.setThreshold(desiredThreshhold)
    return index()

@app.route("/refreshTemperature", methods=["POST"])
def getCurrentTemp():
    # will need to change if a voting system is implemented
    #  manualTemp = thermostat.getTemp()
    thermostat.refreshTemp()
    return index()

"""
    TvLights
"""
@app.route("/tvLights", methods=["POST"])
def tvLights():
    status = request.form["lights"]
    #  print("received:",status)
    
    req = requests.get('http://{}:5000/{}'.format("tvpi", status))

    return index()

@app.route("/restartTv", methods=["POST"])
def restartTv():
    # restarts server - could restart whole pi in future
    #  req = requests.get('http://{}:5000/{}'.format("tvpi", "off"))
    #  req = requests.get('http://{}:5000/{}'.format("tvpi", "on"))

    # restarts whole pi
    req = requests.get(f'http://tvpi:5000/restart')

    return index()

@app.route("/tvColor", methods=["POST"])
def tvColor():
    status = request.form["sync"]

    if status == "off":
        req = requests.get("http://tvpi:5000/color?r=0&g=0&b=0")
    else:
        brightness = rgbStrip1.getBrightness()
        r = int(rgbStrip1.getR() * brightness / 255.0)
        g = int(rgbStrip1.getG() * brightness / 255.0)
        b = int(rgbStrip1.getB() * brightness / 255.0)


        print("rgbStrip settings:",brightness, r,g,b)
        req = requests.get(f"http://tvpi:5000/color?r={r}&g={g}&b={b}")

    return index()

"""
    Automation
"""
@app.route("/automation", methods=["GET"])
def automation():
    acceptableArgs = ["enableAutomation", "treeLight"]

    # get request args and assign to variables
    for arg in request.args:
        if arg in acceptableArgs:
            arg = request.args.get(arg)

    # make changes if enabled 
    if enableAutomation:
        print("automation is enabled")


"""
    Runs app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    
    # on pi
    app.run(host=getIP(), port=80)
