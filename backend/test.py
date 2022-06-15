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
pixels.brightness = 0.5
pixels.fill((255,255,0))
minldr = 1023
maxldr = 0
vorBright = 0
try:
    while True:
        waardeldr = spi.readChannel(2)
        # print(joyX,joyY,waardeldr)
        if(waardeldr < minldr):
            minldr = waardeldr
        if waardeldr > maxldr:
            maxldr = waardeldr
        if maxldr != minldr:
            lichtsterkte = round(100 - (100*((waardeldr - minldr) / (maxldr - minldr))),2)
            print("licht",lichtsterkte)
            if lichtsterkte <= 55:
                pixels.fill((255,255,0))
                bright = 1 -lichtsterkte / 50
                print("in if")
                print("bright",bright,"vorbright",vorBright)
                if abs(bright - vorBright) >0.05 :
                    print("in if2")
                    pixels.brightness = float(bright)
                    vorBright = bright
            else:
                pixels.brightness = 0
        print("brightness",pixels.brightness)
        time.sleep(1)

except KeyboardInterrupt:
    print("KBDSFOIHDSFGHUIOLUQGFGUFIDUGHIFDS")
finally:
    GPIO.cleanup()