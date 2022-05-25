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
buzzer = 26
btn = Button(12)
joyBtn = Button(16)
lcdStatus = 0
vorips = ""
vortijd = "gggggggg"
teller = 0
# objecten
spi = SpiClass(0,0)
lcd = lcdClass(rs,e,None,True)

def lees_knop(pin):
    global lcdStatus,vortijd,vorips
    if btn.pressed:
        lcdStatus += 1
        if lcdStatus >= 2:
            lcdStatus = 0
            vorips = ""
        vortijd = "gggggggg"
        lcd.reset_lcd()

def joy_knop(pin):
    # wordt random ingedrukt
    global lcdStatus
    if joyBtn.pressed:
        print("dfdsfq")
        if lcdStatus == 1 or lcdStatus == 3:
            if lcdStatus == 3:
                lcdStatus = 1
            else:
                lcdStatus = 3
                lcd.set_cursor(4)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    btn.on_press(lees_knop)
    # joyBtn.on_press(joy_knop)

def displayStatus(y,x):
    global lcdStatus, vorips,vortijd,teller
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
        pass
        # if x > 1000:
        #     teller += 1
        #     if teller > vortijd.length():
        #         print("groter")
        #     lcd.set_cursor(4+teller)
        # print(teller)
        # print("X",x,"\nY",y)



try:
    setup()
    while True:
        joyY = spi.readChannel(0)
        joyX = spi.readChannel(1)
        displayStatus(joyY,joyX)

except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
finally:
    lcd.reset_lcd()
    GPIO.cleanup()