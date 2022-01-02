import requests

class lightswitch:
    def __init__(self, ip, name="Lightswitch", inverted=False, selectedBgColor='#ffffff', deselectedBgColor='#dcdcdc', errorColor='#ff4210'):
        self._ip = ip
        self._inverted = inverted
        self._status = "off"

        self._name = name

        self._selectedBgColor = selectedBgColor
        self._deselectedBgColor = deselectedBgColor
        self._errorColor = errorColor

        self._onButtonColor = selectedBgColor
        self._offButtonColor = deselectedBgColor

    def setIP(self, ipaddr):
        self._ip = ipaddr

    def setStatus(self, status):
        self._status = status
        
        if self._inverted:
            if status == 'on':
                status = 'off'
            elif status == 'off':
                status = 'on'

        if status == 'on':
            binStatus = 1
        else:
            binStatus = 0

        try:
            print("Sending request:",'http://{}/switch?light={}'.format(self._ip, binStatus))
            req = requests.get('http://{}/switch?light={}'.format(self._ip, binStatus))
        except:
            print("Couldn't connect to {}".format(self._ip))

            self._onButtonColor = self._errorColor
            self._offButtonColor = self._errorColor

        if status == 'on':
            self._onButtonColor = self._selectedBgColor
            self._offButtonColor = self._deselectedBgColor
        else:
            self._onButtonColor = self._deselectedBgColor
            self._offButtonColor = self._selectedBgColor

    def getOnButtonColor(self):
        return self._onButtonColor

    def getOffButtonColor(self):
        return self._offButtonColor

    def getInfo(self):
        return [
                self._name,
                self._onButtonColor,
                self._offButtonColor,
                self._status,
                ]

