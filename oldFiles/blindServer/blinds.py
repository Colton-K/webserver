from flask import Flask, render_template, request, jsonify, flash, session   # Flask modules 
import socket
# import RPi.GPIO as GPIO
import time

app = Flask(__name__)

blindState = -1

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

def setMotor(change, direction):
    if direction == 'up':
        print("Turning up for {} seconds".format(change * 4))
    elif direction == 'down':
        print("Turning down for {} seconds".format(change * 4))

@app.route("/blinds", methods=["GET","POST"])
def blinds():
    global blindState

    if request.method == 'POST':
        status = request.form["height"]
    else:
        status = request.args.get("height")
    
    change = status - blindState

    if status == 1 and change > 0:
        # calibrate when the blinds go to the base layer with a button or something
        # while (button not pressed)
            # setMotor(.1, 'down')
    # if status == 4 and change > 0: # consider adding a metric to test if it is at the max too

    elif change < 0:
        # moving blinds down
        setMotor(change, 'down')
    elif change > 0:
        # moving blinds up
        setMotor(change, 'up')

    blindState = status

    return index()


@app.route("/")
def index():
    global blindState
    return render_template('index.html', state=blindState)


if __name__ == "__main__":
    # app.run(host=getIP(), port=80)
    app.run() 