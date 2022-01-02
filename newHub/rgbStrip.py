import requests

import asyncio
import datetime
import random
import websockets

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

effectsDict = {
    "none": 0,
    "fade": 1,
    "rgbFade": 2,
    "strobe": 3,
    "running": 4,
    "colorWipe": 5,
    "rainbowCycle": 6,
    "fire": 7,
    "meteorRain": 8,

}

class rgbStrip:
    def __init__(self, ip, name="rgbStrip", onColor='#ffffff', gammaCorrecting=True, offColor='#dcdcdc', errorColor='#ff4210', socketHost=('localhost', 7999)):
        self.ip = ip
        self.socketIP = socketHost[0]
        self.socketPort = socketHost[1]
        print(self.socketIP, self.socketPort)

        self.name = name

        self.r = 255
        self.g = 255
        self.b = 255
        self.brightness = 0

    
        self.onColor = onColor
        self.offColor = offColor
        self.errorColor = errorColor
        self.brightnessButtonBgColors = [onColor, offColor, offColor, offColor]

        self.rgbServerConnected = False
        
        self.gammaCorrecting = gammaCorrecting

    def getInfo(self):
        return [
                self.name,
                self.ip,
                self.r,
                self.g,
                self.b,
                self.brightness,
                self.brightnessButtonBgColors,
                ]

    def getOnColor(self):
        return self.onColor

    def getOffColor(self):
        return self.offColor


    def RGBtoHex(self, r, g, b):
        r = str(hex(r)[2:])
        g = str(hex(g)[2:])
        b = str(hex(b)[2:])


        if len(r) == 1:
            r = '0' + r

        if len(g) == 1:
            g = '0' + g

        if len(b) == 1:
            b = '0' + b
    
        # print('Hex string:','# ' + r + " " + g + " " + b)
        return '#' + r + g + b
    
    def hextoRGB(self, hexString):
        r = int(hexString[1:3], 16)
        g = int(hexString[3:5], 16)
        b = int(hexString[5:7], 16)
        
        return r, g, b

    def setHex(self, hexString):
        r,g,b = self.hextoRGB(hexString)
        self.setRGB(r,g,b)

    def setRGBB(self, r, g, b, brightness):
        tmpr = int(r * brightness / 255.0)
        tmpg = int(g * brightness / 255.0)
        tmpb = int(b * brightness / 255.0)

        if self.gammaCorrecting:
            tmpr = gammaCorrection[tmpr]
            tmpg = gammaCorrection[tmpg]
            tmpb = gammaCorrection[tmpb]

        #  rgbStr = self.RGBtoHex(tmpr, tmpg, tmpb)[1:] # historic

        try:
            _ = requests.get('http://{}/rgb?r={}&g={}&b={}&brightness={}'.format(self.ip,tmpr,tmpg,tmpb,brightness))
            # update vars if successful
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

            if brightness == 0:
                self.brightnessButtonBgColors = [self.onColor, self.offColor, self.offColor, self.offColor]
            elif brightness == 255:
                self.brightnessButtonBgColors = [self.offColor, self.offColor, self.offColor, self.onColor]
            elif brightness > 0 and brightness <=150:
                self.brightnessButtonBgColors = [self.offColor, self.onColor, self.offColor, self.offColor]
            elif brightness > 150 and brightness < 255:
                self.brightnessButtonBgColors = [self.offColor, self.offColor, self.onColor, self.offColor]

            self.rgbServerConnected = True
        except:
            print("Couldn't connect to {}".format(self.ip))
            # set buttons to be error colored    
            self.rgbServerConnected = False
            self.brightnessButtonBgColors = [self.errorColor] * 4

    def setBrightness(self, brightness):
        self.setRGBB(self.r, self.g, self.b, brightness)

    def setRGB(self, r, g, b):
        self.setRGBB(r, g, b, self.brightness)

    def setEffect(self, effect):
        effectNum = effectsDict[effect]

        try:
            req = requests.get('http://{}/effect?effect={}'.format(self.ip, effectNum))

            self.rgbServerConnected = True
        except:
            self.rgbServerConnected = False
            print("Couldn't connect to {}".format(self.ip))

    def getR(self):
        return self.r

    def getG(self):
        return self.g

    def getB(self):
        return self.b

    def getBrightness(self):
        return self.brightness

    def getBrightnessButtonColors(self):
        return self.brightnessButtonBgColors

    def getHex(self):
        return self.RGBtoHex(self.r, self.g, self.b)


    async def processSocket(self, websocket, path):
        while websocket.open:
            message = await websocket.recv()
            print(f"received: {message}")

            m = message.split("|")

            print(m)
            if m[0] == "rgb":
                    self.setHex(m[1])
            elif m[0] == "brightness":
                self.setBrightness(int(m[1]))

            #  await websocket.send("hello world")
            #  await asyncio.sleep(1)

    async def openSocket(self):
        print(f"Serving on {self.socketIP}:{self.socketPort}")
        async with websockets.serve(self.processSocket, self.socketIP, self.socketPort):
            await asyncio.Future()

    #  async def main():
    #      async with websockets.serve(getSliders, "localhost", 7999):
    #          await asyncio.Future()

    #  if __name__ == "__main__":
    #      asyncio.run(main())
