# import matplotlib.pyplot as plt
import plotly.express as px
import plotly
import os

workingDir = os.getcwd()
os.chdir(workingDir)
figPath = workingDir + "/test.html"

def getData():

	with open("temperatures.txt") as fh:
	    file = fh.read()

	entries = file.split("\n")

	times = []
	temps = []
	timetempdict = {}

	for entry in entries:
	    if entry != '':
	        timetemp = entry.split(", ")
	        if int(timetemp[1]) < 100: 
	            times.append(timetemp[0])
	            temps.append(timetemp[1])
	# to put in dictionary
	# for i in range(len(times)):
	#     if int(temps[i]) < 100:
	#         print (int(temps[i]))
	#         timetempdict[times[i]] = temps[i]
    
	return times, temps

def getAverage(list):
	total = 0
	num = 0
	for item in list:
		total += int(item)
		num = num + 1

	return total / num

def smoothData(times, temps):
	# get a 5 point average
	for i in range(1, len(times), 5):
		print(i)
	return times, temps

# get data
times, temps = getData()
average = [getAverage(temps)] * len(temps)
# smoothedX, smoothedY = smoothData[times, temps]
# plot main line
fig = px.line(x=times, y=temps)
# average line
fig.add_scatter(x=times, y=average, mode='lines')
# smooth data
# fig.add_scatter(x=smoothedX, y=smoothedY, mode='lines')
# save plot
plotly.offline.plot(fig, filename=figPath)
# user interface
print("Saved plot to",figPath)