from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import serial # communicate with arduino
import socket

color = 'FFFFFF'
brightness = 0
serConnected = True
effect = 'noEffect'

app = Flask(__name__)

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
    checkRGBStr(str(rgbStrSer.readline()))
    print("Connected to USB0")
except:
    try: 
        rgbStrSer = serial.Serial('/dev/ttyUSB1',9600)
        checkRGBStr(str(rgbStrSer.readline()))
        print("Connected to USB1")
    except:
        try:
            rgbStrSer = serial.Serial('/dev/ttyUSB2',9600)
            checkRGBStr(str(rgbStrSer.readline()))
            print("Connected to USB2")
        except:
            try:
                rgbStrSer = serial.Serial('/dev/ttyUSB3',9600)
                checkRGBStr(str(rgbStrSer.readline()))
                print("Connected to USB3")
            except:
                try:
                    rgbStrSer = serial.Serial('/dev/ttyACM0',9600)
                    checkRGBStr(str(rgbStrSer.readline()))
                    print("Connected to ACM0")
                except:
                    try:
                        rgbStrSer = serial.Serial('/dev/AMA0', 9600)
                        checkRGBStr(str(rgbStrSer.readline()))
                        print("Connected to AMA0")
                    except:
                        try:
                            # print("trying com5")
                            rgbStrSer = serial.Serial('COM5', 9600)
                            checkRGBStr(str(rgbStrSer.readline()))
                            print("Connected to COM5")
                        except:
                            try:
                                rgbStrSer = serial.Serial('COM4', 9600)
                                checkRGBStr(str(rgbStrSer.readline()))
                                print("Connected to COM4")
                            except:
                                print("Unable to connect to serial")
                                serConnected = False

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

def setEffect():
    global effect

    print("effect is:",effect)
    if effect == "rgbFade":
        print("Writing rgb fade ") 
        if serConnected:
            rgbStrSer.write(str.encode('*1^'))
    elif effect == "fade":
        print("Writing colored fade ")
        if serConnected:
            rgbStrSer.write(str.encode('*2^'))
    elif effect == "strobe":
        print("Writing strobe ")
        if serConnected:    
            rgbStrSer.write(str.encode('*3^'))
    else:
        print("Writing no effect")
        if serConnected:
            rgbStrSer.write(str.encode('*0^'))


"""
    set rgb color
"""
def hextoRGB(color):
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return(r,g,b)

def setRGB():
    global color
    global brightness
    
    r,g,b = hextoRGB(color)
    brightness = int(brightness)

    red = int(r * brightness / 255)
    green = int(g * brightness / 255)
    blue = int(b * brightness / 255)

    # set values
    rgbStr = "<" + str(red) + ">" + "-" + str(green) + "_" + "(" + str(blue) + ")"
    if serConnected:
        print("Writing rgbStr: ", rgbStr)
        rgbStrSer.write(str.encode(rgbStr))



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

@app.route("/rgb", methods=["GET","POST"])
def rgb():
    global color
    global brightness
    
    if request.method == 'POST':
        color = request.form["hex"]
        brightness = request.form["brightness"]
    else:
        color = request.args.get("hex")
        brightness = request.args.get("brightness")

    setRGB()

    return index()

@app.route("/effect", methods=["GET", "POST"])
def effect():
    global effect

    if request.method == 'POST':
        effect = request.form["effect"]
    else:
        effect = request.args.get("effect")

    setEffect()

@app.route("/")
def index():
    global color
    global brightness

    return render_template('index.html', backgroundColor="#{}".format(color))


if __name__ == "__main__":
    app.run(host=getIP(), port=80)
    # app.run()