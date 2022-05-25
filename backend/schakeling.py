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
joyBtn = Button(19)
btn = Button(12)
lcdStatus = 0
vorips = ""
vortijd = "gggggggg"
teller = 4
minldr = 1023
maxldr = 0
waardeldr = 0
lichtsterkte = 0
joyTimer = time.time()
wekker = 0
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
    global lcdStatus,vortijd
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
    joyBtn.on_press(joy_knop)

def displayStatus(y,x):
    global lcdStatus, vorips , vortijd , teller , joyTimer , wekker
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
        timer = time.time()
        # print("timer",timer,"joytimer",joyTimer)
        if timer - joyTimer >=0.5:
            # print("test")
            if x > 1000:
                teller += 1
                cijfer = vortijd[teller-4:teller-3]
                # als hij op een : komt 1 skippen
                if cijfer == ":":
                    teller += 1
                # checken als teller groter is dan lengte tijd
                if teller -4  > len(vortijd)-1:
                    print("groter")
                    teller = 4
                lcd.set_cursor(teller)
                joyTimer = time.time()
            elif x < 10:
                teller -= 1
                cijfer = vortijd[teller-4:teller-3]
                # als hij op een : komt 1 skippen
                if cijfer == ":":
                    teller -= 1
                # checken als teller kleiner is dan lengte tijd
                if teller <= 3:
                    print("kleiner")
                    teller = 11
                lcd.set_cursor(teller)
                joyTimer = time.time()
            if y > 1000:
                # cijfer = int(vortijd[teller-4:teller-3])
                # cijfer += 1
                # if cijfer >= 10:
                #     cijfer = 0
                # vortijd = vortijd[0:teller-4] + str(cijfer) + vortijd[teller-3::]
                # print("naar boven",cijfer)
                # lcd.set_cursor(4)
                # lcd.write_message(vortijd)
                # lcd.set_cursor(teller)
                # joyTimer = time.time()
                joyTimer = getal_veranderen(teller,True)
            elif y < 10:
                # cijfer = int(vortijd[teller-4:teller-3])
                # cijfer -= 1
                # if cijfer <= -1:
                #     cijfer = 9
                # # print("test",vortijd[teller-5:teller-4],vortijd[teller-3::])
                # vortijd = vortijd[0:teller-4] + str(cijfer) + vortijd[teller-3::]
                # print("naar beneden",cijfer)
                # lcd.set_cursor(4)
                # lcd.write_message(vortijd)
                # lcd.set_cursor(teller)
                # joyTimer = time.time()
                joyTimer = getal_veranderen(teller)
                

            # print(teller)
        # print("X",x,"\nY",y)

def getal_veranderen(teller,plus=False):
    print("functie")
    global vortijd
    cijfer = int(vortijd[teller-4:teller-3])
    if plus is False:
        cijfer -= 1
    else:
        cijfer +=1
    if cijfer <= -1:
        cijfer = 9
    elif cijfer >= 10:
        cijfer = 0
    # print("test",vortijd[teller-5:teller-4],vortijd[teller-3::])
    vortijd = vortijd[0:teller-4] + str(cijfer) + vortijd[teller-3::]
    print("naar beneden",cijfer)
    lcd.set_cursor(4)
    lcd.write_message(vortijd)
    lcd.set_cursor(teller)
    joyTimer = time.time()
    return joyTimer


try:
    setup()
    while True:
        joyY = spi.readChannel(0)
        joyX = spi.readChannel(1)
        waardeldr = spi.readChannel(2)
        displayStatus(joyY,joyX)
        # ldr
        if(waardeldr < minldr):
            minldr = waardeldr
        if waardeldr > maxldr:
            maxldr = waardeldr
        if maxldr != minldr:
            lichtsterkte = 100 - (100*((waardeldr - minldr) / (maxldr - minldr)))
            # print(f"Lichtsterkte: {lichtsterkte:.2f} %")

except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
finally:
    lcd.reset_lcd()
    GPIO.cleanup()