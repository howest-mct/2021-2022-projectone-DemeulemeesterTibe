import time
from RPi import GPIO
import sys
import neopixel
import board
from helpers.spiclass import SpiClass
buzz = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz, GPIO.OUT)
spi = SpiClass(0,0)
# buzzer = GPIO.PWM(buzz,1000)
# buzzer.start(10)
pixels = neopixel.NeoPixel(board.D18,12)
pixels.brightness = 0
pixels.fill((255,255,0))
minldr = 1023
maxldr = 0
vorBright = 0
timer = time.time()
tijd = time.time()
bright = 0
teller = 0
try:
	while True:
		tijd = time.time()
		# print(tijd - timer)
		if (tijd - timer) >=0.5:
			bright += 0.05
			teller += 0.5
			print(teller)
			if bright >= 0.5:
				bright = 0 
				teller = 0
			timer = time.time()
		# tijd = time.time()
			pixels.brightness = bright
except KeyboardInterrupt:
    print("KBDSFOIHDSFGHUIOLUQGFGUFIDUGHIFDS")
finally:
    GPIO.cleanup()