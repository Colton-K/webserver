from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import serial # communicate with arduino
import os
from time import sleep
import socket
import requests

app = Flask(__name__)

offColor = '#dcdcdc'
onColor = '#ffffff'
errorColor = '#ff4210'

# vars
pwmFreq = 50
oldRGB = [0,0,0,255] # last index is brightness
onButtonBackgroundColor = offColor
offButtonBackgroundColor = onColor
blindButtonBackgroundColors = [onColor, offColor, offColor, offColor]
brightnessButtonBackgroundColors = [offColor, offColor, offColor, onColor]
serConnected = True
password = 'asdf'
test = False
fading = True
testIP = '127.0.0.1:5000'

# files
base = 'index.html'

# connect to RGB strip controller
def checkRGBStr(serStr):
    if "rgbStripThingy" in serStr:
        print('in')
        rgbStrSer.write('y'.encode())
    else:
        print('not rgbStripThingy')
        raise

try:
    rgbStrSer = serial.Serial('/dev/ttyUSB0',9600)
    print("Connected to USB0")
    checkRGBStr(str(rgbStrSer.readline()))
except:
    try: 
        rgbStrSer = serial.Serial('/dev/ttyUSB1',9600)
        print("Connected to USB1")
        checkRGBStr(str(rgbStrSer.readline()))
    except:
        try:
            rgbStrSer = serial.Serial('/dev/ttyUSB2',9600)
            print("Connected to USB2")
            checkRGBStr(str(rgbStrSer.readline()))
        except:
            try:
                rgbStrSer = serial.Serial('/dev/ttyUSB3',9600)
                print("Connected to USB3")
                checkRGBStr(str(rgbStrSer.readline()))
            except:
                try:
                    rgbStrSer = serial.Serial('/dev/ttyACM0',9600)
                    print("Connected to ACM0")
                    checkRGBStr(str(rgbStrSer.readline()))
                except:
                    try:
                        rgbStrSer = serial.Serial('/dev/AMA0', 9600)
                        print("Connected to AMA0")
                        checkRGBStr(str(rgbStrSer.readline()))
                    except:
                        print("Unable to connect to serial")
                        serConnected = False

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
    # adjust variables
    red = int(r * brightness / 255)
    green = int(g * brightness / 255)
    blue = int(b * brightness / 255)

    # set values
    rgbStr = "<" + str(red) + ">" + "-" + str(green) + "_" + "(" + str(blue) + ")"
    if serConnected:
        print("Writing rgbStr")
        rgbStrSer.write(str.encode(rgbStr))
    
    # write old values
    oldRGB[0] = r
    oldRGB[1] = g
    oldRGB[2] = b
    oldRGB[3] = brightness
    
    # debug
    print(rgbStr)

# debug function
def printRGB():
    for i in range(4):
        print("oldRGB[{}] = {}".format(i,oldRGB[i]))

''' 
Fancy effects
'''
def noEffect():
    print("Writing no effect")
    if serConnected:
        rgbStrSer.write(str.encode('*0^'))

def rgbFade():
    print("Writing rgb fade ") 
    if serConnected:
        rgbStrSer.write(str.encode('*1^'))

def fade():
    print("Writing colored fade ")
    if serConnected:
        rgbStrSer.write(str.encode('*2^'))

def strobe():
    print("Writing strobe ")
    if serConnected:
        rgbStrSer.write(str.encode('*3^'))



# display home page
@app.route("/")
def index():
    # overrides password
    if test:
        return render_template(base, r=oldRGB[0], g=oldRGB[1], b=oldRGB[2], brightness=oldRGB[3], color=RGBtoHex(oldRGB[0],oldRGB[1],oldRGB[2]), \
        brightnessButton1BackgroundColor=brightnessButtonBackgroundColors[0], brightnessButton2BackgroundColor=brightnessButtonBackgroundColors[1], brightnessButton3BackgroundColor=brightnessButtonBackgroundColors[2], brightnessButton4BackgroundColor=brightnessButtonBackgroundColors[3], \
        onButtonBackgroundColor=onButtonBackgroundColor, offButtonBackgroundColor=offButtonBackgroundColor, \
        blindButton1BackgroundColor=blindButtonBackgroundColors[0], blindButton2BackgroundColor=blindButtonBackgroundColors[1], blindButton3BackgroundColor=blindButtonBackgroundColors[2], blindButton4BackgroundColor=blindButtonBackgroundColors[3], \
        )

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # return render_template(base, r=oldRGB[0], g=oldRGB[1], b=oldRGB[2], brightness=oldRGB[3], color=RGBtoHex(oldRGB[0],oldRGB[1],oldRGB[2]), onButtonBackgroundColor=onButtonBackgroundColor, offButtonBackgroundColor=offButtonBackgroundColor)
        return render_template(base, r=oldRGB[0], g=oldRGB[1], b=oldRGB[2], brightness=oldRGB[3], color=RGBtoHex(oldRGB[0],oldRGB[1],oldRGB[2]), \
        brightnessButton1BackgroundColor=brightnessButtonBackgroundColors[0], brightnessButton2BackgroundColor=brightnessButtonBackgroundColors[1], brightnessButton3BackgroundColor=brightnessButtonBackgroundColors[2], brightnessButton4BackgroundColor=brightnessButtonBackgroundColors[3], \
        onButtonBackgroundColor=onButtonBackgroundColor, offButtonBackgroundColor=offButtonBackgroundColor, \
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

@app.route("/sliders", methods=["POST"])
def sliders():
    brightness = oldRGB[3]

    # Get slider Values
    r = int(request.form["r"])
    g = int(request.form["g"])
    b = int(request.form["b"])

    # print("Setting R: {} G: {} B: {} Brightness: {}".format(r,g,b, brightness))

    setRGB(r,g,b, brightness)

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

    return index()

@app.route("/button", methods=["POST"])
def button():
    hexString = (request.form["button"])
    r,g,b = hextoRGB(hexString)
    brightness = oldRGB[3]
    setRGB(r,g,b,brightness)
    
    return index()

@app.route("/effects", methods=["POST"])
def effects():
    selectedEffect = (request.form["effect"])

    if selectedEffect == 'fade':
        fade()
    elif selectedEffect == 'strobe':
        strobe()
    elif selectedEffect == 'rgbFade':
        rgbFade()
    else: 
        noEffect()

    return index()

@app.route("/switch", methods=["GET","POST"])
def switch():
    global onButtonBackgroundColor
    global offButtonBackgroundColor

    if test:
        lightSwitchIP = testIP
    else:
        lightSwitchIP = 'thinkSwitch'

    if request.method == 'POST':
        status = request.form["lights"]
    else:
        status = request.args.get("lights")
    
    if status == 'on':
        try:
            req = requests.get('http://{}/switch?lights=on'.format(lightSwitchIP))
            onButtonBackgroundColor = onColor
            offButtonBackgroundColor = offColor
        except:
            print("Couldn't connect to {}".format(lightSwitchIP))
            onButtonBackgroundColor = errorColor
            offButtonBackgroundColor = offColor
    else:
        try:
            req = requests.get('http://{}/switch?lights=off'.format(lightSwitchIP))
            onButtonBackgroundColor = offColor
            offButtonBackgroundColor = onColor
        except:
            print("Couldn't connect to {}".format(lightSwitchIP))
            onButtonBackgroundColor = offColor
            offButtonBackgroundColor = errorColor

    return index()

@app.route("/blinds", methods=["POST"])
def blinds():
    global blindButtonBackgroundColors

    if test:
        blindsIP = testIP
    else:
        blindsIP = '192.168.1.117:80'

    openPercent = int(request.form["blinds"])
    blindButtonBackgroundColors = [offColor] * 4 
    
    if openPercent == 0:
        try:
            blindButtonBackgroundColors[0] = onColor
            req = requests.get('http://{}/blinds?height=1'.format(blindsIP))
        except:
            print("Couldn't connect to {}".format(blindsIP))
            blindButtonBackgroundColors[0] = errorColor
    elif openPercent == 30:
        try:
            blindButtonBackgroundColors[1] = onColor
            req = requests.get('http://{}/blinds?height=2'.format(blindsIP))
        except:
            print("Couldn't connect to {}".format(blindsIP))
            blindButtonBackgroundColors[1] = errorColor
    elif openPercent == 60:
        try:
            blindButtonBackgroundColors[2] = onColor
            req = requests.get('http://{}/blinds?height=3'.format(blindsIP))
        except:
            print("Couldn't connect to {}".format(blindsIP))
            blindButtonBackgroundColors[2] = errorColor
    elif openPercent == 100:
        try:
            blindButtonBackgroundColors[3] = onColor
            req = requests.get('http://{}/blinds?height=4'.format(blindsIP))
        except:
            print("Couldn't connect to {}".format(blindsIP))
            blindButtonBackgroundColors[3] = errorColor

    return index()

# Run the app
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    
    # on dev device
    test = True
    # app.run()
    
    # on pi
    app.run(host=getIP(), port=80)