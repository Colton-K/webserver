from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import serial # communicate with arduino
import os
from time import sleep
import socket
import requests
import datetime

from smartFan import smartFan
from rgbStrip import rgbStrip
from smartLight import smartLight
from lightswitch import lightswitch

app = Flask(__name__)

# initialize fans
smartFans = []
fanIPs = []
for fanIP in fanIPs:
    smartFans.append(smartFan(fanIP))

# init rgbStrip
rgbStrip1 = rgbStrip('192.168.11.73')

# initialize smart lights
smartLights = []
lightIPs = ['192.168.11.6', '192.168.11.7'] # 192.168.11.5
for lightIP in lightIPs:
    smartLights.append(smartLight(lightIP))

# init lightswitches for old fashioned lights
lightswitches = []
lightswitchIPs = ['192.168.11.5']
for lightswitchIP in lightswitchIPs:
    lightswitches.append(lightswitch(lightswitchIP))


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

    return render_template(base, r=rgbStrip1.getR(), g=rgbStrip1.getG(), b=rgbStrip1.getB(), brightness=rgbStrip1.getBrightness(), color=rgbStrip1.getHex(), \
    brightnessButton1BackgroundColor=rgbStrip1.getBrightnessButtonColors()[0], brightnessButton2BackgroundColor=rgbStrip1.getBrightnessButtonColors()[1], brightnessButton3BackgroundColor=rgbStrip1.getBrightnessButtonColors()[2], brightnessButton4BackgroundColor=rgbStrip1.getBrightnessButtonColors()[3], \
    numFans=len(smartFans), \
    fan1OnButtonBackgroundColor=fanOnColors[0], fan1OffButtonBackgroundColor=fanOffColors[0], \
    fan2OnButtonBackgroundColor=fanOnColors[1], fan2OffButtonBackgroundColor=fanOffColors[1], \
    fan3OnButtonBackgroundColor=fanOnColors[2], fan3OffButtonBackgroundColor=fanOffColors[2], \
    numLights=len(smartLights), \
    light1OnButtonBackgroundColor=lightOnColors[0], light1OffButtonBackgroundColor=lightOffColors[0], \
    light2OnButtonBackgroundColor=lightOnColors[1], light2OffButtonBackgroundColor=lightOffColors[1], \
    light3OnButtonBackgroundColor=lightOnColors[2], light3OffButtonBackgroundColor=lightOffColors[2], \
    numSwitches=len(lightswitches), \
    ls1OnBgColor=lightswitchOnColors[0], ls1OffBgColor=lightswitchOffColors[0], \
    ls2OnBgColor=lightswitchOnColors[1], ls2OffBgColor=lightswitchOffColors[1], \
    )
    
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
@app.route("/fans", methods=["POST"])
def fans():
    status = request.form["fans"]

    for fan in smartFans:
        #change status of fan
        fan.setStatus(status)

    return index()
    

# toggle switches
def handleToggle(fanIndex):
    smartFans[fanIndex].invertStatus()


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
    

# toggle switches
def handleToggle(lightIndex):
    smartLights[lightIndex].invertStatus()


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
