from cgitb import reset
from helpers.lcdClass import lcdClass
from helpers.klasseknop import Button
from helpers.spiclass import SpiClass
from subprocess import check_output
from RPi import GPIO
import time

# variabelen
rs = 21
e =  20
btn = Button(12)
joyBtn = Button(16)
lcdStatus = 0
vorips = ""
vortijd = "gggggggg"
# objecten
spi = SpiClass(0,0)
lcd = lcdClass(rs,e,None,True)

def lees_knop(pin):
    global lcdStatus,vortijd
    if btn.pressed:
        lcdStatus += 1
        if lcdStatus >= 2:
            lcdStatus = 0
        vortijd = "gggggggg"
        lcd.reset_lcd()
        print(lcdStatus)

def joy_knop(pin):
    global lcdStatus,vortijd
    if joyBtn.pressed:
        if lcdStatus == 1 or lcdStatus == 3:
            if lcdStatus == 3:
                lcdStatus = 1
            else:
                lcdStatus = 3
            lcd.reset_lcd()
        vortijd = "gggggggg"

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rs, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    btn.on_press(lees_knop)
    joyBtn.on_press(joy_knop)

def displayStatus():
    global lcdStatus, vorips,vortijd
    if lcdStatus == 0:
        lcd.reset_cursor()
        ips = check_output(["hostname", "-I"])
        ips = ips.decode("utf-8")
        lijst = ips.split()
        if ips != vorips:
            print("nieuw ip")
            for i in range(0, 2):
                if (i % 2) == 0:
                    lcd.second_row()
                else:
                    lcd.first_row()
                lcd.write_message(lijst[i])
        vorips = ips
    elif lcdStatus == 1:
        tijd = time.strftime("%H:%M:%S")
        if vortijd != tijd:
            t = 0
            for (a, b) in zip(tijd, vortijd):
                if a !=b:
                    lcd.set_cursor(4+t)
                    lcd.write_message(a)
                t += 1
        vortijd = tijd
    elif lcdStatus == 3:
        lcd.write_message("test")



try:
    setup()
    while True:
        displayStatus()
        print(spi.readChannel(0))
        print(spi.readChannel(1))
        time.sleep(1)

except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
finally:
    lcd.reset_lcd()
    GPIO.cleanup()