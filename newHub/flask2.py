#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import os
from time import sleep
import socket
import requests
import datetime
import threading
import asyncio

from smartFan import smartFan
from rgbStrip import rgbStrip
from smartLight import smartLight
from lightswitch import lightswitch
#  from smartThermostat import smartThermostat
#  from tvLight import tvLight

app = Flask(__name__)
socketPort = 7998

lightswitchIPs = ['192.168.11.11']
fanIPs = ['192.168.11.5','192.168.11.6', '192.168.11.7']
lightIPs = [] #['192.168.11.7'] 
rgbStripIP = '192.168.11.10'
#  thermostatIP = '192.168.11.13'
#  tvpiIP, tvpiPort = 'tvpi', 5000


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
    #  return 'localhost'

# initialize fans
smartFans = []
for i, fanIP in enumerate(fanIPs):
    smartFans.append(smartFan(fanIP, name=f"smartFan{i}"))

# init rgbStrip
rgbStrip1 = rgbStrip(rgbStripIP, socketHost=(getIP(), socketPort))

# initialize smart lights
smartLights = []
for lightIP in lightIPs:
    smartLights.append(smartLight(lightIP, offon=True))

# init lightswitches for old fashioned lights
lightswitches = []
for lightswitchIP in lightswitchIPs:
    lightswitches.append(lightswitch(lightswitchIP, inverted=True))

# init thermostat
#  thermostat = smartThermostat(thermostatIP)

# init tvLight
#  tvpi = tvLight(tvpiIP, tvpiPort, syncEnabled=False)

# files
base = 'index.html'



"""
    Display home page
"""
@app.route("/")
def index():
    # things to return in template
    values = {
            "rgbInfo" : [rgbStrip1.getInfo()],
            "color" : rgbStrip1.getHex(),
            "oncolor" : rgbStrip1.getOnColor(),
            "offcolor" : rgbStrip1.getOffColor(),
            "fanInfo" : [fan.getInfo() for fan in smartFans],
            "lightSwitchInfo" : [ls.getInfo() for ls in lightswitches],
            "smartLightInfo" : [ls.getInfo() for ls in smartLights],
            "socketHostname" : getIP(),
            "socketPort" : socketPort,
            }

    return render_template(base, **values)
    
#  @app.route('/login', methods=['POST'])
#  def login():
#      if request.form['password'] == password:
#          session['logged_in'] = True
#      else:
#          flash('Wrong password!')
#      return index()
 
#  # not included anywhere yet
#  @app.route("/logout")
#  def logout():
#      session['logged_in'] = False
#      return index()


"""
    RGB SUBSYSTEM
"""
def setRGB(hexString):
    r,g,b = rgbStrip1.hextoRGB(hexString)
    rgbStrip1.setRGB(r,g,b)

    if tvpi.syncIsEnabled:
        tvpi.setRGB(r,g,b)
    

def setBrightness(level):
    rgbStrip1.setBrightness(int(level))

    #  if tvpi.syncIsEnabled():
        #  tvpi.setBrightness(level)

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
#  @app.route("/tempControl", methods=["POST"])
#  def tempControl():
#      status = request.form["status"]
#      thermostat.setStatus(status)
#      return index()

#  @app.route("/setDesiredTemp", methods=["POST"])
#  def setDesiredTemp():
#      desiredTemp = request.form["temp"]
#      thermostat.setTemp(desiredTemp)
#      return index()

#  @app.route("/setDesiredThreshold", methods=["POST"])
#  def setDesiredThreshold():
#      desiredThreshhold = request.form["t5hreshold"]
#      thermostat.setThreshold(desiredThreshhold)
#      return index()

#  @app.route("/refreshTemperature", methods=["POST"])
#  def getCurrentTemp():
#      # will need to change if a voting system is implemented
#      #  manualTemp = thermostat.getTemp()
#      thermostat.refreshTemp()
#      return index()

"""
    TvLights
"""
#  @app.route("/tvLights", methods=["POST"])
#  def tvLights():
#      status = request.form["lights"]
#      #  print("received:",status)
    
#      tvpi.setLightStatus(status)
#      #  req = requests.get('http://{}:5000/{}'.format("tvpi", status))

#      return index()

#  @app.route("/restartTv", methods=["POST"])
#  def restartTv():
#      # restarts whole pi
#      #  req = requests.get(f'http://tvpi:5000/restart')

#      tvpi.restart()

#      return index()

#  @app.route("/toggleSync", methods=["POST"])
#  def tvColor():
#      tvpi.toggleSync()

#      return index()

"""
    Automation
"""
#  @app.route("/automation", methods=["GET"])
#  def automation():
#      acceptableArgs = ["enableAutomation", "treeLight"]

#      # get request args and assign to variables
#      for arg in request.args:
#          if arg in acceptableArgs:
#              arg = request.args.get(arg)

#      # make changes if enabled 
#      if enableAutomation:
#          print("automation is enabled")


async def runSocket():
    import rgbSocket

    await rgbSocket.main()


#  threading.Thread(target=asyncio.run(rgbStrip1.openSocket())).start()
threading.Thread(target=asyncio.run,args=[rgbStrip1.openSocket()]).start()

"""
    Runs app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    #  asyncio.run(rgbStrip1.openSocket())
    #  print(getIP(), socketPort)

    app.run(host='192.168.1.133', port=80)
    #  app.run(host=getIP(), port=80)
    #  app.run()
    
