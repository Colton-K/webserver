from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import serial # communicate with arduino
import os
from time import sleep
import socket
import requests
import datetime

app = Flask(__name__)

offColor = '#dcdcdc'
onColor = '#ffffff'
errorColor = '#ff4210'

# vars
overridePassword = True

pwmFreq = 50
oldRGB = [0,0,0,255] # last index is brightness
fan1OnButtonBackgroundColor = offColor
fan1OffButtonBackgroundColor = onColor
fan2OnButtonBackgroundColor = offColor
fan2OffButtonBackgroundColor = onColor
fan3OnButtonBackgroundColor = offColor
fan3OffButtonBackgroundColor = onColor
status1 = 'off'
status2 = 'off'
status3 = 'off'
onButtonBackgroundColor = offColor
offButtonBackgroundColor = onColor
blindButtonBackgroundColors = [onColor, offColor, offColor, offColor]
brightnessButtonBackgroundColors = [offColor, offColor, offColor, onColor]
serConnected = True
password = 'asdf'
fading = True
rgbServer = '192.168.10.21'
fan1IP = '192.168.11.5'
fan2IP = '192.168.11.6'
fan3IP = '192.168.11.7'
gammaCorrection = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
    115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
    144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
    177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
    215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]

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

def RGBtoHex(r,g,b):
    r = str(hex(r)[2:])
    g = str(hex(g)[2:])
    b = str(hex(b)[2:])

    if len(r) == 1:
        r = '0' + r

    if len(g) == 1:
        g = '0' + g

    if len(b) == 1:
        b = '0' + g
    elif len(b) == 0:
        print('b is')

    return '#' + r + g + b

def hextoRGB(hexString):
    r = int(hexString[1:3], 16)
    g = int(hexString[3:5], 16)
    b = int(hexString[5:7], 16)
    return(r,g,b)

def setRGB(r,g,b,brightness): 

    # write old values
    oldRGB[0] = r
    oldRGB[1] = g
    oldRGB[2] = b
    oldRGB[3] = brightness
    
    # set values
    rgbStr = RGBtoHex(r,g,b)[1:]
    # get ip
    rgbIP = rgbServer
    # send request to server
    try:
        req = requests.get('http://{}/rgb?hex={}&brightness={}'.format(rgbIP,rgbStr,brightness))
    except:
        print("Couldn't connect to {}".format(rgbIP))

def setRGBGammaCorrected(r, g, b, brightness):
    # write old values
    oldRGB[0] = r
    oldRGB[1] = g
    oldRGB[2] = b
    oldRGB[3] = brightness
    
    r = gammaCorrection[r]
    g = gammaCorrection[g]
    b = gammaCorrection[b]

    # set values
    rgbStr = RGBtoHex(r,g,b)[1:]
    
    # get ip
    rgbIP = rgbServer
    # send request to server
    try:
        req = requests.get('http://{}/rgb?hex={}&brightness={}'.format(rgbIP,rgbStr,brightness))
    except:
        print("Couldn't connect to {}".format(rgbIP))

def setEffect(effect):
    r = oldRGB[0]
    g = oldRGB[1]
    b = oldRGB[2]
    brightness = oldRGB[3]

    # get ip
    rgbIP = rgbServer
    # send request to server
    try:
        req = requests.get('http://{}/effect?effect={}'.format(rgbIP,effect))
        print("Sending req: ", req)
    except:
        print("Couldn't connect to {}".format(rgbIP))
    
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
        return render_template(base, r=oldRGB[0], g=oldRGB[1], b=oldRGB[2], brightness=oldRGB[3], color=RGBtoHex(oldRGB[0],oldRGB[1],oldRGB[2]), \
        brightnessButton1BackgroundColor=brightnessButtonBackgroundColors[0], brightnessButton2BackgroundColor=brightnessButtonBackgroundColors[1], brightnessButton3BackgroundColor=brightnessButtonBackgroundColors[2], brightnessButton4BackgroundColor=brightnessButtonBackgroundColors[3], \
        lightsOnButtonBackgroundColor=onButtonBackgroundColor, lightsOffButtonBackgroundColor=offButtonBackgroundColor, \
        fan1OnButtonBackgroundColor=fan1OnButtonBackgroundColor, fan1OffButtonBackgroundColor=fan1OffButtonBackgroundColor, \
        fan2OnButtonBackgroundColor=fan2OnButtonBackgroundColor, fan2OffButtonBackgroundColor=fan2OffButtonBackgroundColor, \
        fan3OnButtonBackgroundColor=fan3OnButtonBackgroundColor, fan3OffButtonBackgroundColor=fan3OffButtonBackgroundColor, \
        blindButton1BackgroundColor=blindButtonBackgroundColors[0], blindButton2BackgroundColor=blindButtonBackgroundColors[1], blindButton3BackgroundColor=blindButtonBackgroundColors[2], blindButton4BackgroundColor=blindButtonBackgroundColors[3], \
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
    brightness = oldRGB[3]

    # Get slider Values
    r = int(request.form["r"])
    g = int(request.form["g"])
    b = int(request.form["b"])

    # print("Setting R: {} G: {} B: {} Brightness: {}".format(r,g,b, brightness))

    # setRGB(r,g,b, brightness)
    setRGBGammaCorrected(r,g,b, brightness)

    return index()

@app.route("/button", methods=["POST"])
def button():
    hexString = (request.form["button"])
    r,g,b = hextoRGB(hexString)
    brightness = oldRGB[3]
    setRGB(r,g,b,brightness)
    # setRGBGammaCorrected(r,g,b, brightness)
    
    return index()

@app.route("/brightness", methods=["POST"])
def brightness():
    global brightnessButtonBackgroundColors

    r,g,b = oldRGB[0],oldRGB[1],oldRGB[2]
    brightness = int(request.form["brightness"])
    
    brightnessButtonBackgroundColors = [offColor] * 4

    if brightness == 0:
        brightnessButtonBackgroundColors[0] = onColor 
    elif brightness == 77:
        brightnessButtonBackgroundColors[1] = onColor
    elif brightness == 153:
        brightnessButtonBackgroundColors[2] = onColor
    elif brightness == 255:
        brightnessButtonBackgroundColors[3] = onColor

    setRGB(r,g,b,brightness)
    # setRGBGammaCorrected(r,g,b, brightness)

    return index()

@app.route("/effects", methods=["POST"])
def effects():
    selectedEffect = (request.form["effect"])
    setEffect(selectedEffect)

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
    global fan1IP
    global status1
    global fan1OnButtonBackgroundColor
    global fan1OffButtonBackgroundColor
    global fan2IP
    global status2
    global fan2OnButtonBackgroundColor
    global fan2OffButtonBackgroundColor
    global fan3IP
    global status3
    global fan3OnButtonBackgroundColor
    global fan3OffButtonBackgroundColor

    status1 = request.form["fans"]
    status2 = request.form["fans"]
    status3 = request.form["fans"]

    # change status of fans
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan1IP, status1))
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan2IP, status2))
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan3IP, status3))

    # update html pagew
    if status1 == 'on':
        fan1OnButtonBackgroundColor = onColor
        fan1OffButtonBackgroundColor = offColor
    elif status1 == 'off':
        fan1OnButtonBackgroundColor = offColor
        fan1OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    if status2 == 'on':
        fan2OnButtonBackgroundColor = onColor
        fan2OffButtonBackgroundColor = offColor
    elif status2 == 'off':
        fan2OnButtonBackgroundColor = offColor
        fan2OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    if status3 == 'on':
        fan3OnButtonBackgroundColor = onColor
        fan3OffButtonBackgroundColor = offColor
    elif status3 == 'off':
        fan3OnButtonBackgroundColor = offColor
        fan3OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

# toggle switches
@app.route("/fan1toggle", methods=["GET", "POST"])
def fan1toggle():
    global fan1IP
    global status1
    global fan1OnButtonBackgroundColor
    global fan1OffButtonBackgroundColor

    if status1 == "on":
        status1 = "off"
    else:
        status1 = "on"

    # change status of fans
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan1IP, status1))
    print(fan1IP, status1)

    # update html pagew
    if status1 == 'on':
        fan1OnButtonBackgroundColor = onColor
        fan1OffButtonBackgroundColor = offColor
    elif status1 == 'off':
        fan1OnButtonBackgroundColor = offColor
        fan1OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

@app.route("/fan2toggle", methods=["POST"])
def fan2toggle():
    global fan2IP
    global status2
    global fan1OnButtonBackgroundColor
    global fan1OffButtonBackgroundColor

    if status2 == "on":
        status2 = "off"
    else:
        status2 = "on"

    # change status of fans
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan2IP, status2))
    print(fan2IP, status2)
    
    # update html pagew
    if status2 == 'on':
        fan2OnButtonBackgroundColor = onColor
        fan2OffButtonBackgroundColor = offColor
    elif status2 == 'off':
        fan2OnButtonBackgroundColor = offColor
        fan2OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

@app.route("/fan3toggle", methods=["POST"])
def fan3toggle():
    global fan3IP
    global status3
    global fan1OnButtonBackgroundColor
    global fan1OffButtonBackgroundColor

    if status3 == "on":
        status3 = "off"
    else:
        status3 = "on"

    # change status of fans
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan3IP, status3))
    print(fan3IP, status3)

    # update html pagew
    if status3 == 'on':
        fan3OnButtonBackgroundColor = onColor
        fan3OffButtonBackgroundColor = offColor
    elif status3 == 'off':
        fan3OnButtonBackgroundColor = offColor
        fan3OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

# bottom on/off switches
@app.route("/fan1", methods=["GET", "POST"])
def fan1():
    global fan1IP
    global status1
    global fan1OnButtonBackgroundColor
    global fan1OffButtonBackgroundColor

    if request.method == 'POST':
        status1 = request.form["fan1"]
    else:
        status1 = request.args.get("status1")

    print(status1)

    # change status of fans
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan1IP, status1))

    # update html pagew
    if status1 == 'on':
        fan1OnButtonBackgroundColor = onColor
        fan1OffButtonBackgroundColor = offColor
    elif status1 == 'off':
        fan1OnButtonBackgroundColor = offColor
        fan1OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

@app.route("/fan2", methods=["POST"])
def fan2():
    global fan2IP
    global status2
    global fan2OnButtonBackgroundColor
    global fan2OffButtonBackgroundColor

    status2 = request.form["fan2"]
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan2IP, status2))

    # update html pagew
    if status2 == 'on':
        fan2OnButtonBackgroundColor = onColor
        fan2OffButtonBackgroundColor = offColor
    elif status2 == 'off':
        fan2OnButtonBackgroundColor = offColor
        fan2OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

    return index()

@app.route("/fan3", methods=["POST"])
def fan3():
    global fan3IP
    global status3
    global fan3OnButtonBackgroundColor
    global fan3OffButtonBackgroundColor

    status3 = request.form["fan3"]
    os.system("./tplink_smartplug.py -t {} -c {}".format(fan3IP, status3))

    # update html pagew
    if status3 == 'on':
        fan3OnButtonBackgroundColor = onColor
        fan3OffButtonBackgroundColor = offColor
    elif status3 == 'off':
        fan3OnButtonBackgroundColor = offColor
        fan3OffButtonBackgroundColor = onColor
    else:
        print("Fan input unknown.")

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