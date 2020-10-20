import requests
from time import sleep

url = "http://192.168.1.117:80/"

req = requests.get('http://192.168.1.117/switch?lights=off')
# req = requests.get('http://192.168.1.117/switch?lights=on')

print(type(req))