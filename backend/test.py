from helpers.lcdClass import lcdClass
from helpers.klasseknop import Button
from helpers.spiclass import SpiClass
from RPi import GPIO
import time


rs = 21
e =  20
btn = Button(12)
joyBtn = Button(16)
spi = SpiClass(0,0)

def lees_knop(pin):
    if btn.pressed:
        print("test")
def joy_knop(pin):
    if joyBtn.pressed:
        print("test")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rs, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    btn.on_press(lees_knop)
    joyBtn.on_press(joy_knop)

try:
    setup()
    lcd = lcdClass(rs,e,None,True)
    while True:
        lcd.write_message("a")
        print(spi.readChannel(0))
        print(spi.readChannel(1))
        time.sleep(2)

except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
finally:
    GPIO.cleanup()