from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import serial # communicate with arduino
import os
from time import sleep
import socket
import requests
import datetime

from smartFan import smartFan
from rgbStrip import rgbStrip

app = Flask(__name__)

'''
offColor = '#dcdcdc'
onColor = '#ffffff'
errorColor = '#ff4210'
'''

# vars
overridePassword = True

#pwmFreq = 50
oldRGB = [0,0,0,255] # last index is brightness

# initialize fans
smartFans = []
fanIPs = ['192.168.11.5', '192.168.11.6', '192.168.11.7']

for fanIP in fanIPs:
    smartFans.append(smartFan(fanIP))


rgbStrip1 = rgbStrip('192.168.11.72')


serConnected = True
password = 'asdf'

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
    # global fan1OnButtonBackgroundColor
    # global fan1OffButtonBackgroundColor
    # global fan2OnButtonBackgroundColor
    # global fan2OffButtonBackgroundColor
    # global fan3OnButtonBackgroundColor
    # global fan3OffButtonBackgroundColor
    # overrides password
    if overridePassword:
        return render_template(base, r=rgbStrip1.getR(), g=rgbStrip1.getG(), b=rgbStrip1.getB(), brightness=rgbStrip1.getBrightness(), color=rgbStrip1.getHex(), \
        brightnessButton1BackgroundColor=rgbStrip1.getBrightnessButtonColors()[0], brightnessButton2BackgroundColor=rgbStrip1.getBrightnessButtonColors()[1], brightnessButton3BackgroundColor=rgbStrip1.getBrightnessButtonColors()[2], brightnessButton4BackgroundColor=rgbStrip1.getBrightnessButtonColors()[3], \
        fan1OnButtonBackgroundColor=smartFans[0].getOnButtonColor(), fan1OffButtonBackgroundColor=smartFans[0].getOffButtonColor(), \
        fan2OnButtonBackgroundColor=smartFans[1].getOnButtonColor(), fan2OffButtonBackgroundColor=smartFans[1].getOffButtonColor(), \
        fan3OnButtonBackgroundColor=smartFans[2].getOnButtonColor(), fan3OffButtonBackgroundColor=smartFans[2].getOffButtonColor(), \
        #blindButton1BackgroundColor=blindButtonBackgroundColors[0], blindButton2BackgroundColor=blindButtonBackgroundColors[1], blindButton3BackgroundColor=blindButtonBackgroundColors[2], blindButton4BackgroundColor=blindButtonBackgroundColors[3], \
        )

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template(base, r=oldRGB[0], g=oldRGB[1], b=oldRGB[2], brightness=oldRGB[3], color=RGBtoHex(oldRGB[0],oldRGB[1],oldRGB[2]), \
        brightnessButton1BackgroundColor=brightnessButtonBackgroundColors[0], brightnessButton2BackgroundColor=brightnessButtonBackgroundColors[1], brightnessButton3BackgroundColor=brightnessButtonBackgroundColors[2], brightnessButton4BackgroundColor=brightnessButtonBackgroundColors[3], \
        lightsOnButtonBackgroundColor=onButtonBackgroundColor, lightsOffButtonBackgroundColor=offButtonBackgroundColor, \
        fan1OnButtonBackgroundColor=fan1OnButtonBackgroundColor, fan1OffButtonBackgroundColor=fan1OffButtonBackgroundColor, \
        fan2OnButtonBackgroundColor=fan2OnButtonBackgroundColor, fan2OffButtonBackgroundColor=fan2OffButtonBackgroundColor, \
        fan3OnButtonBackgroundColor=fan3OnButtonBackgroundColor, fan3OffButtonBackgroundColor=fan3OffButtonBackgroundColor, \
        blindButton1BackgroundColor=blindButtonBackgroundColors[0], blindButton2BackgroundColor=blindButtonBackgroundColors[1], blindButton3BackgroundColor=blindButtonBackgroundColors[2], blindButton4BackgroundColor=blindButtonBackgroundColors[3], \
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

@app.route("/effects", methods=["POST"])
def effects():
    selectedEffect = (request.form["effect"])
    effect(selectedEffect)

    return index()

"""
    SWITCH SUBSYSTEM
"""
# @app.route("/switch", methods=["GET","POST"])
# def switch():
#     global onButtonBackgroundColor
#     global offButtonBackgroundColor

#     if test:
#         lightSwitchIP = testIP
#     else:
#         lightSwitchIP = 'thinkSwitch'

#     if request.method == 'POST':
#         status = request.form["lights"]
#     else:
#         status = request.args.get("lights")
    
#     if status == 'on':
#         try:
#             req = requests.get('http://{}/switch?lights=on'.format(lightSwitchIP))
#             onButtonBackgroundColor = onColor
#             offButtonBackgroundColor = offColor
#         except:
#             print("Couldn't connect to {}".format(lightSwitchIP))
#             onButtonBackgroundColor = errorColor
#             offButtonBackgroundColor = offColor
#     else:
#         try:
#             req = requests.get('http://{}/switch?lights=off'.format(lightSwitchIP))
#             onButtonBackgroundColor = offColor
#             offButtonBackgroundColor = onColor
#         except:
#             print("Couldn't connect to {}".format(lightSwitchIP))
#             onButtonBackgroundColor = offColor
#             offButtonBackgroundColor = errorColor

#     return index()

"""
    BLINDS SUBSYSTEM
"""
# @app.route("/blinds", methods=["POST"])
# def blinds():
#     global blindButtonBackgroundColors

#     if test:
#         blindsIP = testIP
#     else:
#         blindsIP = '192.168.1.117:80'

#     openPercent = int(request.form["blinds"])
#     blindButtonBackgroundColors = [offColor] * 4 
    
#     if openPercent == 0:
#         try:
#             blindButtonBackgroundColors[0] = onColor
#             req = requests.get('http://{}/blinds?height=1'.format(blindsIP))
#         except:
#             print("Couldn't connect to {}".format(blindsIP))
#             blindButtonBackgroundColors[0] = errorColor
#     elif openPercent == 30:
#         try:
#             blindButtonBackgroundColors[1] = onColor
#             req = requests.get('http://{}/blinds?height=2'.format(blindsIP))
#         except:
#             print("Couldn't connect to {}".format(blindsIP))
#             blindButtonBackgroundColors[1] = errorColor
#     elif openPercent == 60:
#         try:
#             blindButtonBackgroundColors[2] = onColor
#             req = requests.get('http://{}/blinds?height=3'.format(blindsIP))
#         except:
#             print("Couldn't connect to {}".format(blindsIP))
#             blindButtonBackgroundColors[2] = errorColor
#     elif openPercent == 100:
#         try:
#             blindButtonBackgroundColors[3] = onColor
#             req = requests.get('http://{}/blinds?height=4'.format(blindsIP))
#         except:
#             print("Couldn't connect to {}".format(blindsIP))
#             blindButtonBackgroundColors[3] = errorColor

#     return index()

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
        status = request.args.get("status")
    
    # update fan
    smartFans[0].setStatus(status)
    
    return index()

@app.route("/fan2", methods=["GET", "POST"])
def fan2():
    # get status
    if request.method == 'POST':
        status = request.form["fan"]
    else:
        status = request.args.get("status")
    
    # update fan
    smartFans[1].setStatus(status)
   
    return index()

@app.route("/fan3", methods=["GET", "POST"])
def fan3():
    # get status
    if request.method == 'POST':
        status = request.form["fan"]
    else:
        status = request.args.get("status")
    
    # update fan
    smartFans[2].setStatus(status)
    
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
    Runs app
"""
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    
    # on dev device
    # app.run()
    
    # on pi
    app.run(host=getIP(), port=80)
