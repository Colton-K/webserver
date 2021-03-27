import requests

class smartThermostat:
    def __init__(self, ip="", desiredTemp = 58, desiredThreshold = 5, selectedBgColor = '#ffffff', deselectedBgColor = '#dcdcdc', errorColor = '#ff4210'):
        self.status = 0
        self.ip = ip
        self.desiredTemp = desiredTemp
        self.desiredThreshold = desiredThreshold

        self.deselectedBgColor = deselectedBgColor
        self.selectedBgColor = selectedBgColor
        self.errorColor = errorColor

        self.onButtonColor = deselectedBgColor
        self.offButtonColor = selectedBgColor

    def getTargetTemp(self):
        return self.desiredTemp

    def setIP(self, ipaddr):
        self.ip = ipaddr

    def setStatus(self, status):
        if status == "on":
            status = 1
        elif status == "off":
            status = 0

        try: 
            req = requests.get("http://{}/tempcontrol?status={}".format(self.ip, status))
            self.status = status
            
            if status:
                self.onButtonColor = self.selectedBgColor
                self.offButtonColor = self.deselectedBgColor
            else:
                self.onButtonColor = self.deselectedBgColor
                self.offButtonColor = self.selectedBgColor

        except:
            print("Couldn't connect to {}".format(self.ip))

    def getTemp(self):
        # get last line of temperatures.txt
        with open('temperatures.txt', 'r') as fh:
            temps = fh.readlines()
            return temps[-1]

    def getThreshold(self):
        return self.desiredThreshold

    def setTemp(self, desiredTemp):
        try: 
            req = requests.get("http://{}/settemp?temp={}".format(self.ip, desiredTemp))
            self.desiredTemp = desiredTemp
        except:
            print("Couldn't connect to {}".format(self.ip))
            
    
    def setThreshold(self, desiredThreshold):
        try: 
            req = requests.get("http://{}/setthreshold?temp={}".format(self.ip, desiredThreshold))
            self.desiredThreshold = desiredThreshold
        except:
            print("Couldn't connect to {}".format(self.ip))

    def refreshTemp(self):
        try:
            req = requests.get("http://{}/currentTemp".format(self.ip))
        except:
            print("Couldn't connect to {}".format(self.ip))

