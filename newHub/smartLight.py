import os
import time

class smartLight:
    def __init__(self, ip='', offon=False, selectedBgColor = '#ffffff', deselectedBgColor = '#dcdcdc', errorColor = '#ff4210'):
        self.status = 'off'
        self.ip = ip
        self.offon = offon

        self.deselectedBgColor = deselectedBgColor
        self.selectedBgColor = selectedBgColor
        self.errorColor = errorColor

        self.onButtonColor = deselectedBgColor
        self.offButtonColor = selectedBgColor

    def setIP(self, ipaddr):
        self.ip = ipaddr

    def setStatus(self, status):
        self.status = status
        
        # control the switch
        # print("status:", status)
        os.system("./tplink_smartplug.py -t {} -c {}".format(self.ip, self.status))
        
        time.sleep(.5)
        if self.offon:
            os.system("./tplink_smartplug.py -t {} -c {}".format(self.ip, 'on'))
            status = 'on'
            self.status = 'on'

        # update color
        if status == 'on':
            self.onButtonColor = self.selectedBgColor
            self.offButtonColor = self.deselectedBgColor
        else:
            self.onButtonColor = self.deselectedBgColor
            self.offButtonColor = self.selectedBgColor    

    def invertStatus(self):
        if self.status == 'on':
            self.setStatus('off')
        else:
            self.setStatus('on')

    def getIP(self):
        return self.ip

    def getStatus(self):
        return self.status

    def getOnButtonColor(self):
        return self.onButtonColor

    def getOffButtonColor(self):
        return self.offButtonColor
