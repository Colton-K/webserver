import os

class smartFan:
    def __init__(self, ip='', name="Smart Fan", selectedBgColor = '#ffffff', deselectedBgColor = '#dcdcdc', errorColor = '#ff4210'):
        self.status = 'off'
        self.ip = ip
        self.name = name
        self.status = 'off'

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
        os.system("./tplink_smartplug.py -t {} -c {}".format(self.ip, self.status))
        
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

    def getInfo(self):
        return [
                self.name,
                self.onButtonColor,
                self.offButtonColor,
                self.status
                ]
