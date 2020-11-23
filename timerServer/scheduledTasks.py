import time
import requests

while(True):
    hour = list(time.localtime())[3]
    minute = list(time.localtime())[4]

    if hour == 10 and minute > 0 and minute < 15:
        print("turning on tree light")
        req = requests.get('http://192.168.11.19/light3?light=on')
    elif hour == 23 and minute > 45 and minute < 59:
        print("turning off tree light")
        req = requests.get('http://192.168.11.19/light3?light=off')

    time.sleep(60)
