class lightswitch:
    def __init__(self, ip, selectedBgColor='#ffffff', deselectedBgColor='#dcdcdc', errorColor='#ff4210'):
        self.ip = ip

        self.selectedBgColorColor = selectedBgColor
        self.deselectedBgColor = deselectedBgColor
        self.errorColor = errorColor

        self.onButtonColor = selectedBgColor
        self.offButtonColor = deselectedBgColor

    def setIP(self, ipaddr):
        self.ip = ipaddr

    def setStatus(self, status):
        self.status = status
        
        if status == 'on':
            binStatus = 1
        else:
            binStatus = 0
    
        try:
            req = requests.get('httpL//{}/switch?light={}'.format(self.ip, binStatus))
        except:
            print("Couldn't connect to {}".format(self.ip))

            self.onButtonColor = self.errorColor
            self.offButtonColor = self.errorColor

        if status == 'on':
            self.onButtonColor = selectedColor
            self.offButtonColor = deselectedColor
        else:
            self.onButtonColor = deselectedColor
            self.offButtonColor = selectedColor

    def getOnButtonColor(self):
        return self.onButtonColor

    def getOffButtonColor(self):
        return self.offButtonColor


