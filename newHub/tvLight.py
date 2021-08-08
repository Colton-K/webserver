#!/bin/python3

import requests

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

class tvLight:
    def __init__(self, ip, port, onColor="#40ff4c", gammaCorrection=True, syncEnabled=False, offColor="#ffadad", errorColor="#ff4210"):
        self.ip = ip
        self.port = port
        self.onColor = onColor
        self.offColor = offColor
        self.gammaCorrecting = gammaCorrection

        self.syncEnabled = syncEnabled

        self.r = 255
        self.g = 255
        self.b = 255
        self.brightness = 0

    def syncIsEnabled(self):
        if self.syncEnabled:
            #  print("sync is enabled")
            return True
        else:
            #  print("sync is disabled")
            return False

        
    def getSyncButtonColor(self):
        print(self.syncEnabled)
        if self.syncEnabled:
            return self.onColor
        
        return self.offColor

    def setLightStatus(self, status):
        print("status:", status)
        req = requests.get(f'http://{self.ip}:{self.port}/{status}')

        if status == "Off": # make sure they are actually turning off
            self.syncEnabled = False
            self.setRGBB(0,0,0,0)

    def setRGBB(self, r, g, b, brightness):
        r, g, b, brightness = int(r), int(g), int(b), int(brightness)

        self.r = r
        self.g = g
        self.b = b
        self.brightness = brightness

        r = int(r * brightness / 255.0)
        g = int(g * brightness / 255.0)
        b = int(b * brightness / 255.0)

        if self.gammaCorrecting:
            r = gammaCorrection[r]
            g = gammaCorrection[g]
            b = gammaCorrection[b]

        
        print(f"setting rgbb: http://{self.ip}:{self.port}/color?r={r}&g={g}&b={b}")
        req = requests.get(f"http://{self.ip}:{self.port}/color?r={r}&g={g}&b={b}")

    def setRGB(self, r, g, b):
        self.setRGBB(r,g,b,self.brightness)

    def setBrightness(self, brightness):
        self.setRGBB(self.r,self.g,self.b,brightness)

    def toggleSync(self):
        self.syncEnabled = not self.syncEnabled
        print("toggleSync changed sync to:", self.syncEnabled)

    def restart(self):
        req = requests.get(f'http://{self.ip}:{self.port}/restart')

if __name__ == "__main__":
    tv = tvLight("tvpi", 5000)

    tv.syncIsEnabled()
    tv.toggleSync()
    tv.syncIsEnabled()

