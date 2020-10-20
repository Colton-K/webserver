from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import socket
import time
try:
    import RPi.GPIO as GPIO

    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    # p.ChangeDutyCycle(0)
    p.stop()
    GPIO.cleanup()

    pi = True
except:
    print("This is not a raspberry pi!")
    pi = False
    
desiredStatus = 'off'
currentStatus = 'off'
# servo positions
up = 10 # 90 degrees
neutral = 7.5 # neutral position
down = 5 # -90 degrees

app = Flask(__name__)

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

def setServo(on):
    global currentStatus

    if pi:
        if currentStatus == 'off' and on:
            p.ChangeDutyCycle(up)
            currentStatus = 'on'
        elif currentStatus == 'on' and not on:
            p.ChangeDutyCycle(down)
            currentStatus = 'off'
        
        time.sleep(.5)
        p.ChangeDutyCycle(neutral)
    else:
        print(currentStatus, on)
        if currentStatus == 'off' and on:
            print('moving up')
            currentStatus = 'on'
        elif currentStatus == 'on' and not on:
            print('moving down')
            currentStatus = 'off'

        time.sleep(.5)
        print('moving neutral')

@app.route("/switch", methods=["GET","POST"])
def switch():
    global desiredStatus
    if request.method == 'POST':
        desiredStatus = request.form["lights"]
    else:
        desiredStatus = request.args.get("lights")
    
    return index()

@app.route("/")
def index():
    if desiredStatus == 'on':
        setServo(on=True)
        return render_template('index.html', backgroundColor="green")
    else:
        setServo(on=False)
        return render_template('index.html', backgroundColor="red")


if __name__ == "__main__":
    app.run(host=getIP(), port=80)
    # app.run()