from helpers.lcdClass import lcdClass
from helpers.klasseknop import Button
from helpers.spiclass import SpiClass
from subprocess import check_output
# from hx711 import HX711
from RPi import GPIO
import time

# variabelen
dtWeight = 6
clkWeight = 13

alarmopScherm = True
rs = 21
e =  20
buzz = 26
buzzer = ""
joyBtn = Button(19)
btn = Button(12)
lcdStatus = 0
vorips = ""
huidigetijd = 0
tijd = ""
teller = 4
minldr = 1023
maxldr = 0
waardeldr = 0
lichtsterkte = 0
joyTimer = time.time()
alarm = "14:32:10"
aan = False
# objecten
spi = SpiClass(0,0)
lcd = lcdClass(rs,e,None,True)
# hx = HX711(dtWeight,clkWeight)

def lees_knop(pin):
    global lcdStatus,tijd,vorips
    if btn.pressed:
        lcdStatus += 1
        if lcdStatus >= 2:
            lcdStatus = 0
            vorips = ""
        tijd = "gggggggg"
        lcd.reset_lcd()

def joy_knop(pin):
    # wordt random ingedrukt
    global lcdStatus,tijd,alarm,alarmopScherm
    if joyBtn.pressed:
        if lcdStatus == 1 or lcdStatus == 3:
            if lcdStatus == 3:
                lcdStatus = 1
                alarm = tijd
                alarmopScherm = True
                print("alarm",alarm)
            else:
                lcdStatus = 3
                lcd.set_cursor(4)

def setup():
    global buzzer
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz, GPIO.OUT)
    buzzer = GPIO.PWM(buzz,440)
    buzzer.start(0)
    btn.on_press(lees_knop)
    joyBtn.on_press(joy_knop)

def displayStatus(lcdStatus,y,x):
    global vorips , tijd , teller , joyTimer , alarmopScherm, huidigetijd
    if lcdStatus == 0:
        lcd.reset_cursor()
        ips = check_output(["hostname", "-I"])
        ips = ips.decode("utf-8")
        lijst = ips.split()
        if ips != vorips:
            for i in range(0, len(lijst)):
                if i <2:
                    if (i % 2) == 0:
                        lcd.second_row()
                    else:
                        lcd.first_row()
                    lcd.write_message(lijst[i])
        vorips = ips
    elif lcdStatus == 1:
        if tijd != huidigetijd:
            t = 0
            for (a, b) in zip(huidigetijd, tijd):
                if a !=b:
                    lcd.set_cursor(4+t)
                    lcd.write_message(a)
                t += 1
            tijd = huidigetijd
        if alarmopScherm is True:
            print("test")
            lcd.set_cursor(64)
            lcd.write_message(f"Alarm: {alarm}")
            test = False
            
    elif lcdStatus == 3:
        timer = time.time()
        if timer - joyTimer >=0.5:
            if x > 1000:
                teller += 1
                cijfer = tijd[teller-4:teller-3]
                # als hij op een : komt 1 skippen
                if cijfer == ":":
                    teller += 1
                # checken als teller groter is dan lengte tijd
                if teller -4  > len(tijd)-1:
                    print("terug naar begin\t",len(tijd))
                    teller = 4
                lcd.set_cursor(teller)
                joyTimer = time.time()
            elif x < 10:
                teller -= 1
                cijfer = tijd[teller-4:teller-3]
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
                joyTimer = getal_veranderen(teller,tijd)
            elif y < 10:
                joyTimer = getal_veranderen(teller,tijd,True)

def getal_veranderen(teller,vortijd,plus=False):
    global tijd
    cijfer = int(tijd[teller-4])
    if plus is False:
        cijfer -= 1
    else:
        cijfer +=1
    if cijfer <= -1:
        cijfer = 9
    elif cijfer >= 10:
        cijfer = 0
    tijd = tijd[0:teller-4] + str(cijfer) + tijd[teller-3::]
    # lcd.set_cursor(4)
    # lcd.write_message(tijd)
    tijd = checkdeel(tijd)
    # print("#", tijd)
    t = 0
    for (a, b) in zip(vortijd, tijd):
        if a !=b:
            lcd.set_cursor(4+t)
            lcd.write_message(b)
        t += 1
    lcd.set_cursor(teller)
    joyTimer = time.time()
    return joyTimer

def checkdeel(tijd):
    delen = tijd.split(":")
    string = ""
    for deel in range(0,len(delen)):
        if deel == 0:
            # print("M",delen[deel])
            if int(delen[deel]) >= 24:
                delen[deel] = "23"
        else:
            # print("N",delen[deel])
            # if int(delen[deel]) == 90:
            #     delen[deel] = "60"
            if int(delen[deel]) >= 60:
                delen[deel] = "59"
            
        string += str(delen[deel])
        if deel != 2:
            string += ":"
    # print(">", string)
    return string

try:
    setup()
    while True:
        huidigetijd = time.strftime("%H:%M:%S")
        joyY = spi.readChannel(0)
        joyX = spi.readChannel(1)
        displayStatus(lcdStatus,joyY,joyX)
        # ldr
        waardeldr = spi.readChannel(2)
        if(waardeldr < minldr):
            minldr = waardeldr
        if waardeldr > maxldr:
            maxldr = waardeldr
        if maxldr != minldr:
            lichtsterkte = 100 - (100*((waardeldr - minldr) / (maxldr - minldr)))
            # print(f"Lichtsterkte: {lichtsterkte:.2f} %")
        # print(huidigetijd,alarm)
        if huidigetijd == alarm:
            aan = True
        if aan == True:
            print("buzzen")

except KeyboardInterrupt:
    print ('KeyboardInterrupt exception is caught')
finally:
    lcd.reset_lcd()
    GPIO.cleanup()