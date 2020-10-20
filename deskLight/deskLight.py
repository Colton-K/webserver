import scrollphathd
import time
import requests
import sys

width = 17
height = 7

def setBrightness(brightness):
    if brightness != 0:
        for row in range(height):
            for led in range(width):
                if row % 2 == 0 and led % (1/brightness) == 0:
                    scrollphathd.set_pixel(led, row, 1)
                elif row % 2 == 1 and (led + 1) % (1/brightness) == 0:
                    scrollphathd.set_pixel(led, row, 1)
                else:
                    scrollphathd.set_pixel(led, row, 0)
    else:
        scrollphathd.fill(brightness)

    scrollphathd.show()

while True:
    # brightness = float(input("What brightness? "))
    brightness = float(sys.argv[1])
    setBrightness(brightness)
    time.sleep(.001)