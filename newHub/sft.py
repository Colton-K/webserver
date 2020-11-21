from smartFan import smartFan

smartfans = []

fanIPs = ['192.168.1.116', '192.168.1.110', '192.168.1.100']

for fanIP in fanIPs:
    smartfans.append(smartFan(fanIP))

for fan in smartfans: 
    print(fan.getIP())



smartfans[0].setStatus('on')

for fan in smartfans:
    print(fan, fan.getOnButtonColor(), fan.getOffButtonColor())
