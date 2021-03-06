import sys
import time
from tracemalloc import start
from RPi import GPIO
from numpy import average
from helpers.lcdClass import lcdClass
from helpers.klasseknop import Button
from helpers.spiclass import SpiClass
from hx711 import HX711
from datetime import datetime,timedelta
import threading
from subprocess import check_output
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository
import neopixel
import board
import os

from selenium import webdriver
# lcd.reset_cursor()
        # ips = check_output(["hostname", "-I"])
        # ips = ips.decode("utf-8")
        # lijst = ips.split()
            # for i in range(0, len(lijst)):
        #         if i <2:
        #             if (i % 2) == 0:
        #                 lcd.second_row()
        #             else:
        #                 lcd.first_row()
        #             lcd.write_message(lijst[i])
# ifconfig = check_output(['ifconfig', "wlan0"])
# for line in ifconfig.decode().split('\n'):
#     fields = line.split()
#     if fields[0] == 'inet':
#         wifiIp = fields[1]  
#         break
# ifconfig = check_output(['ifconfig', "eth0"])
# for line in ifconfig.decode().split('\n'):
#     fields = line.split()
#     if fields[0] == 'inet':
#         lanIp = fields[1]  
#         break
# print("wifi",wifiIp,"lan",lanIp )
# variabelen
beginTijdSlapen = None
beginTijdSlapenLater = None
eindTijdSlapen = None
dtWeight = 6
clkWeight = 5
wekkers = []
Red = 255
Green = 0
Blue = 0
rs = 21
e =  20
buzz = 26
buzzer = ""
lcdStatus = 1
vorips = ""
huidigetijd = "fddfsdf"
tijd = ""
teller = 4
minldr = 1023
maxldr = 0
waardeldr = 0
lichtsterkte = 0
alarm = ""
timer = 0
vorBright = 0
aan = False
ring = False
showtekst = False
GaanSlapen = False
alarmopScherm = False
autoBrightness = False
rgbStilletjesAan = False
rgbStilletjesUit = False
startbright = False
gewichtmetingen = []
averagegewicht = -100000
WakkerWorden = "Wakker worden!!!"
vorWakkerWorden = ""
# objecten
timenow = datetime.now().replace(microsecond=0)
joyTimer = time.time()
timerldr = time.time()
timerRGB = time.time()
timeLCDStatus = time.time()
joyBtn = Button(19)
btn = Button(12,700)
knopSlapen = Button(17,700)
knopShutdown = Button(27)
spi = SpiClass(0,0)
lcd = lcdClass(rs,e,None,True)
pixels = neopixel.NeoPixel(board.D18,12)
pixels.brightness = 0.5
hx = HX711(dtWeight,clkWeight)
lcd.write_message("Opstarten")
time.sleep(10)
lcd.reset_lcd()
# Code voor Hardware
def setup_gpio():
    global buzzer
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz, GPIO.OUT)
    buzzer = GPIO.PWM(buzz,1000)
    buzzer.ChangeFrequency(1000)
    buzzer.start(0)
    btn.on_press(lees_knop)
    joyBtn.on_press(joy_knop)
    knopSlapen.on_press(Slaap_knop)
    knopShutdown.on_press(Shutdown_knop)

def Slaap_knop(pin):
    print("-------------------------------------------------------")
    global beginTijdSlapen, eindTijdSlapen, GaanSlapen,lcdStatus,timeLCDStatus,tijd,alarmopScherm,rgbStilletjesUit,rgbStilletjesAan
    GaanSlapen = not GaanSlapen
    print("slaap",GaanSlapen)
    if GaanSlapen == 1:
        print("Slaapwel")
        rgbStilletjesUit = True
        beginTijdSlapen = datetime.now().replace(microsecond=0)
        tekstOpLcd("Slaapwel!")
    elif GaanSlapen == 0:
        print("Hallo")
        eindTijdSlapen = datetime.now().replace(microsecond=0)
        timeChecker(beginTijdSlapen,eindTijdSlapen)
        tekstOpLcd("Goeiemorgen")
        rgbStilletjesAan = True
    socketio.emit("B2F_SlaapStatus",{"slapen": GaanSlapen},broadcast=True)

def Shutdown_knop(pin):
    print("Shutdown")
    lcd.reset_lcd()
    pixels.deinit()
    lcd.write_message("Afsluiten")
    time.sleep(2)
    # os.system("sudo poweroff -h now")
    # sys.exit()
    lcd.reset_lcd()
    check_output(["sudo","shutdown","-h","now"])

def lees_knop(pin):
    global lcdStatus,tijd,vorips,alarmopScherm
    if btn.pressed:
        if lcdStatus == 3:
            lcd.disable_cursor()
        lcdStatus += 1
        if lcdStatus >= 2:
            lcdStatus = 0
            vorips = ""
            if wekkers:
                alarmopScherm = True
        tijd = "gggggggg"
        lcd.reset_lcd()

def joy_knop(pin):
    global lcdStatus,tijd,alarm,alarmopScherm,wekkers
    if joyBtn.pressed:
        if lcdStatus == 1 or lcdStatus == 3:
            if lcdStatus == 3:
                lcdStatus = 1
                alarm = tijd
                alarm = datetime.strptime(alarm,"%H:%M:%S")
                alarm = alarm.replace(year=datetime.now().year,month=datetime.now().month,day=datetime.now().day)
                alarm = alarm + timedelta(days=1)
                t = DataRepository.insert_alarm("Alarm",alarm,True,"")
                socketio.emit("B2F_Addalarm",broadcast=True)
                # data = DataRepository.read_alarmen_nog_komen()
                # print("#",data)
                # wekkers = []
                # for w in data:
                #     wekkers.append(w["tijd"])
                # print(">",wekkers[0])
                Wekkers()
                print("alarm",alarm,"\n",alarm)
                lcd.disable_cursor()
                alarmopScherm = True
            else:
                lcd.enable_cursor()
                lcdStatus = 3
                lcd.set_cursor(4)

def codeSchakeling():
    global beginTijdSlapenLater,rgbStilletjesUit,eindTijdSlapen,autoBrightness,startbright,timerRGB,rgbStilletjesAan,ring,minldr,maxldr,aan,timer,timerldr,pixels,huidigetijd,timenow,alarmopScherm,GaanSlapen,beginTijdSlapen,lcdStatus,showtekst,lichtsterkte,vorBright
    Wekkers()
    if wekkers:
        alarmopScherm = True
    while True: 
        timer = time.time()
        huidigetijd = time.strftime("%H:%M:%S")
        timenow = datetime.now().replace(microsecond=0)
        joyY = spi.readChannel(1)
        joyX = spi.readChannel(0)
        # ldr
        waardeldr = spi.readChannel(2)
        if(waardeldr < minldr):
            minldr = waardeldr
        if waardeldr > maxldr:
            maxldr = waardeldr
        if maxldr != minldr:
            lichtsterkte = round(100 - (100*((waardeldr - minldr) / (maxldr - minldr))),2)
        if timer - timerldr >= 60:
            print("LDR inlezen") 
            timerldr = time.time()
            insert = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),lichtsterkte,None,2,1)
            data = DataRepository.read_historiek_by_id(insert)
            print("LDR",lichtsterkte)
        # alarm 
        if wekkers:
            if timenow == (wekkers["tijd"] - timedelta(seconds=11)):
                print("jaaaa")
                if startbright == False:
                    print("gelijk")
                    rgbStilletjesAan = True
                    pixels.brightness = 0
                    timerRGB = time.time()
                    startbright = True
            if timenow == wekkers["tijd"]:
                if showtekst == False:
                    startbright = True
                    print("fffffff")
                    lcd.reset_lcd()
                    aan = True
                    lcdStatus = 5
                    showtekst = True
                    eindTijdSlapen = datetime.now().replace(microsecond=0)
                    print("WEKKER GAAT AF")
        if timenow == beginTijdSlapenLater:
            tekstOpLcd("Slaapwel!")
            rgbStilletjesUit = True
            beginTijdSlapen = beginTijdSlapenLater
            beginTijdSlapenLater = beginTijdSlapenLater - timedelta(seconds=10)
            GaanSlapen = 1
            socketio.emit("B2F_SlaapStatus",{"slapen": GaanSlapen},broadcast=True)
        if aan == True:
            buzzer.start(10)
        displayStatus(joyY,joyX)
        if rgbStilletjesAan != False:
            if autoBrightness == True:
                autoBrightness = False
                socketio.emit("B2F_autoBrightness",{"autobrightness": autoBrightness})
            if (timer - timerRGB) >=0.25:
                if ring == False:
                    ring = True
                    socketio.emit("B2F_Ringstatus",{"ring": ring})
                    id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,3)
                pixels.fill((Red,Green,Blue))
                timerRGB = time.time()
                pixels.brightness += 0.025
                # print(pixels.brightness)
                if pixels.brightness == 1:
                    rgbStilletjesAan = False
                    d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),round(pixels.brightness,2),None,4,5)
                socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
        elif rgbStilletjesUit != False:
            if autoBrightness == True:
                autoBrightness = False
                socketio.emit("B2F_autoBrightness",{"autobrightness": autoBrightness})
            if ring == True:
                if (timer - timerRGB) >=0.25:
                    if pixels.brightness < 0.025:
                        rgbStilletjesUit = False
                        ring = False
                        socketio.emit("B2F_Ringstatus",{"ring": ring})
                        id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,4)
                    else:
                        # print("#",pixels.brightness)
                        pixels.brightness = pixels.brightness - 0.05
                        socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
                        d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),round(pixels.brightness,2),None,4,5)
                    timerRGB = time.time()
            else:
                rgbStilletjesUit = False
                if pixels.brightness != 0:
                    pixels.brightness = 0
                    socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
                    d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),round(pixels.brightness,2),None,4,5)

        else:
            if autoBrightness == False:
                if ring == 1:
                    pixels.fill((Red,Green,Blue))
                elif ring == 0:
                    pixels.fill((0,0,0))
            else:
                if lichtsterkte <= 51:
                    if (timer - timerRGB) >=0.25:
                        pixels.fill((Red,Green,Blue))
                        bright = 1 -lichtsterkte / 50
                        if ring == False:
                            ring = True
                            socketio.emit("B2F_Ringstatus",{"ring": ring})
                            id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,3)
                        if abs(bright - vorBright) >0.05 :
                            pixels.brightness = float(bright)
                            vorBright = bright
                            socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
                            d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),round(pixels.brightness,2),None,4,5)
                        timerRGB = time.time()
                else:
                    if pixels.brightness != 0:
                        pixels.brightness = 0
                        socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
                    if ring == True:
                        ring = False
                        socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
                        socketio.emit("B2F_Ringstatus",{"ring": ring})
                        id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,4)
                        d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),round(pixels.brightness,2),None,4,5)

def displayStatus(y,x):
    global vorips , tijd , teller , joyTimer , alarmopScherm, huidigetijd,timer, vorWakkerWorden,timeLCDStatus,lcdStatus
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
            # print(tijd)
            for (a, b) in zip(huidigetijd, tijd):
                if a !=b:
                    lcd.set_cursor(4+t)
                    lcd.write_message(a)
                t += 1
            tijd = huidigetijd
        if wekkers:
            if alarmopScherm is True:
                print("nieuw alarm")
                lcd.set_cursor(64)
                print("@",wekkers["tijd"].time())
                lcd.write_message(f"Alarm: {wekkers['tijd'].time()}")
                alarmopScherm = False
    elif lcdStatus == 3:
        if timer - joyTimer >=0.3:
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
    elif lcdStatus == 5:
        if vorWakkerWorden != WakkerWorden:
            lcd.first_row()
            lcd.write_message(WakkerWorden)
        vorWakkerWorden = WakkerWorden
    elif lcdStatus == 6:
        # print(timer,"\t",timeLCDStatus,"\t",timer-timeLCDStatus)
        if (timer - timeLCDStatus) >=3:
            print("verander display")
            lcdStatus = 1
            lcd.reset_lcd()

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

def getWeight():
    global averagegewicht,gewichtmetingen,aan,eindTijdSlapen,GaanSlapen,beginTijdSlapen, lcdStatus,vorWakkerWorden,showtekst,tijd
    # hx.set_scale_ratio(hx.get_data_mean(20)/188.0)
    timergewicht = time.time()
    while True:
        # while aan == True:
        # print(round(hx.get_weight_mean(20),2), 'g')
        reading = hx.get_raw_data_mean(10)
        if aan == False:
            gewichtmetingen.append(reading)
            if len(gewichtmetingen) == 5:
                averagegewicht = average(gewichtmetingen)
                print("gemiddelde",averagegewicht)
                gewichtmetingen = []
                # print(">",averagegewicht,"\t#",gewichtmetingen)
            timergewicht = time.time()  
        else:
            diff = averagegewicht - reading
            print("#",diff)
            if diff < -5000:
                print(">",timer - timergewicht)
                if timer - timergewicht >= 2:
                    print("ALARM UIT")
                    aan = False
                    buzzer.start(0)
                    tijd = "gggggggg"
                    lcd.reset_lcd()
                    showtekst = False
                    vorWakkerWorden = ""
                    lcdStatus = 1
                    print("id wekker",wekkers["alarmID"])
                    if wekkers["herhaal"] != "":
                        dagenoverlopen = True
                        tijdstip = wekkers["tijd"]
                        while dagenoverlopen is True:
                            tijdstip = tijdstip + timedelta(days=1)
                            if tijdstip.strftime("%A") in wekkers["herhaal"]:
                                print("NIEUWE DATUM",tijdstip)
                                te = DataRepository.update_alarm_tijdstip_by_id(wekkers["alarmID"],tijdstip)
                                socketio.emit("B2F_Addalarm",broadcast=True)
                                dagenoverlopen = False
                    else:
                        f = DataRepository.update_alarmActief0_by_id(wekkers["alarmID"])
                        print("jaauihdfsulighazuiefzghuizefgui")
                    socketio.emit("B2F_Addalarm",broadcast=True)
                    if beginTijdSlapen:
                        effectievetijd = datetime.now().replace(microsecond=0)
                        print("eindTijdSlapen")
                        timeChecker(beginTijdSlapen,eindTijdSlapen,effectievetijd)
                        # dat = DataRepository.insert_slaap(beginTijdSlapen,eindTijdSlapen,effectievetijd)
                        socketio.emit("B2F_NewSleepData",broadcast=True)
                        GaanSlapen = 0
                        socketio.emit("B2F_SlaapStatus",{"slapen": GaanSlapen},broadcast=True)
                        beginTijdSlapen = None
                    Wekkers()
            else:
                timergewicht = time.time()  
            print("diff",diff)

def Wekkers():
    global wekkers,alarmopScherm,tijd
    if lcdStatus == 2:
        lcd.reset_lcd()
    wekkers = DataRepository.read_alarm_nog_komen()
    print("W0",wekkers)
    if wekkers:
        alarmopScherm = True
    tijd = "gggggggg"

def timeChecker(begin,einde,effectief=None):
    verschil = einde - begin
    if (verschil.total_seconds() /60) >=1:
        print("---- Nieuwe Slaap data ----")
        dat = DataRepository.insert_slaap(begin,einde,effectief)
        socketio.emit("B2F_NewSleepData",broadcast=True)
        print("New sleepdata id:",dat)
    else:
        print("---- Geen Slaap data ----")
        socketio.emit("B2F_NewSleepData",broadcast=True)
    print("Difference",verschil.total_seconds())

def tekstOpLcd(tekst):
    global lcdStatus, timeLCDStatus, tijd, alarmopScherm
    lcd.reset_lcd()
    lcdStatus = 6
    timeLCDStatus = time.time()
    lcd.set_cursor(3)
    lcd.write_message(tekst)
    tijd = "gggggggg"
    if wekkers:
        alarmopScherm = True
# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)



# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/api/alarm/',methods=["GET","POST"])
def alarmen():
    if request.method == "GET":
        data = DataRepository.read_alarmen()
        if data is not None:
            return jsonify(alarmen=data),200
    elif request.method == "POST":
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        data = DataRepository.insert_alarm(gegevens["naam"],gegevens["tijd"],gegevens["actief"],gegevens["herhaal"])
        return jsonify(alarmid=data),201

@app.route('/api/alarm/<alarmid>/',methods=["GET","PUT","DELETE"])
def alarmbyid(alarmid):
    if request.method == "GET":
        data = DataRepository.read_alarm_by_id(alarmid)
        if data is not None:
            return jsonify(alarm=data),200
        else:
            return jsonify(status="error"),404
    elif request.method == "DELETE":
        dele = DataRepository.delete_alarm_by_id(alarmid)
        return jsonify(status=dele),201

@app.route('/api/historiek/',methods=["GET","POST"])
def historiek():
    if request.method == "POST":
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        data = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),gegevens["color"],None,gegevens["deviceID"],gegevens["actieID"])
        return jsonify(historiekID=data),201

@app.route('/api/slaap/',methods=["GET"])
def slaap():
    if request.method == "GET":
        data = DataRepository.read_slaap()
        if data is not None:
            return jsonify(slaap=data),200

@app.route('/api/slaap/week/',methods=["GET"])
def slaapweek():
    if request.method == "GET":
        data = DataRepository.read_slaap_1week()
        if data is not None:
            return jsonify(slaap=data),200

@app.route('/api/slaap/maand/',methods=["GET"])
def slaapmaand():
    if request.method == "GET":
        data = DataRepository.read_slaap_1maand()
        if data is not None:
            return jsonify(slaap=data),200

@app.route('/api/slaap/wekkerdiff/',methods=["GET"])
def slaapWekkerDiff():
    if request.method == "GET":
        data = DataRepository.read_slaap_wekker_diff()
        if data is not None:
            return jsonify(slaap=data),200
# socket endpoints


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    socketio.emit("B2F_Ringstatus",{"ring": ring})
    socketio.emit("B2F_SlaapStatus",{"slapen": GaanSlapen})
    socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness})
    socketio.emit("B2F_SetColor",{"red":Red,"green":Green,"blue":Blue})
    socketio.emit("B2F_autoBrightness",{"autobrightness": autoBrightness})
    

@socketio.on("F2B_SetColor")
def setColor(payload):
    global Red,Green,Blue
    print("---------- Set Color ----------")
    RGB = payload["color"].split(",")
    Red = int(RGB[0])
    Green = int(RGB[1])
    Blue = int(RGB[2])
    print("RGB",Red,Green,Blue)
    socketio.emit("B2F_SetColor",{"red":Red,"green":Green,"blue":Blue},broadcast=True)

@socketio.on("F2B_RGBring")
def setRing(payload):
    global ring
    ring = payload["aan"]
    if payload["aan"] == 1:
        id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,3)
    else:
        id = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,4)
    socketio.emit("B2F_Ringstatus",{"ring":payload["aan"]})

@socketio.on("F2B_Addalarm")
def addAlarm(payload):
    global alarmopScherm
    Wekkers()
    socketio.emit("B2F_Addalarm",broadcast=True)

@socketio.on("F2B_SetBrightness")
def setBrightness(payload):
    pixels.brightness = float(payload["brightness"])
    d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),pixels.brightness,None,4,5)
    socketio.emit("B2F_SetBrightness",{"brightness": payload["brightness"]},broadcast=True)

@socketio.on("F2B_DELalarm")
def delAlarm(payload):
    global alarmopScherm,tijd
    dele = DataRepository.delete_alarm_by_id(payload["alarmid"])
    print(dele)
    Wekkers()

    socketio.emit("B2F_Addalarm",broadcast=True)

@socketio.on("F2B_UpdateAlarm")
def updateAlarm(payload):
    print("*** Update alarm ***")
    dele = DataRepository.update_alarm_by_id(payload["alarmid"],payload["naam"],payload["tijdstip"],payload["actief"],payload["herhaal"])
    Wekkers()
    socketio.emit("B2F_Addalarm",broadcast=True)

@socketio.on("F2B_GaanSlapen")
def setSlaap(payload):
    print("----------------------------")
    # checken of de tijden gelijk zijn voor GaanSlapen inteststellen
    global beginTijdSlapen, eindTijdSlapen,GaanSlapen,beginTijdSlapenLater,rgbStilletjesUit,rgbStilletjesAan
    uur = str(datetime.now().hour)
    if len(uur) == 1:
        uur = "0"+uur
    minut = str(datetime.now().minute)
    if len(minut) == 1:
        minut = "0"+minut
    tijd = uur + ":" + minut
    print("#",payload,tijd)
    if payload["Slapen"] == 1:
        print("#",payload["Slapen"],tijd)
        if payload["tijd"] == tijd:
            print("test")
            tekstOpLcd("Slaapwel!")
            rgbStilletjesUit = True
            GaanSlapen = 1
            beginTijdSlapen = datetime.now().replace(microsecond=0)
            print(beginTijdSlapen)
        else:
            print("andere tijd")
            uur = int(payload["tijd"][0:2])
            minuten = int(payload["tijd"][3:5])
            print("uur",uur,"min",minuten)
            beginTijdSlapenLater = datetime.now().replace(hour=uur,minute=minuten,second=0,microsecond=0)
            if(beginTijdSlapenLater < datetime.now()) == True:
                beginTijdSlapenLater += timedelta(days=1)
                print(beginTijdSlapenLater)
            print(beginTijdSlapenLater)
    # GaanSlapen = payload["Slapen"]
    # print(payload["Slapen"])
    # if GaanSlapen == 1:
    #     beginTijdSlapen = datetime.now().replace(microsecond=0)
    #     print(beginTijdSlapen)
    elif payload["Slapen"] == 0:
        GaanSlapen = 0
        eindTijdSlapen = datetime.now().replace(microsecond=0)
        rgbStilletjesAan = True
        print(eindTijdSlapen)
        tekstOpLcd("Goeiemorgen")
        timeChecker(beginTijdSlapen,eindTijdSlapen)
    # print(GaanSlapen)
    socketio.emit("B2F_SlaapStatus",{"slapen": GaanSlapen},broadcast=True)
    print("@",rgbStilletjesAan,"#",rgbStilletjesUit)

@socketio.on("F2B_setautobrightness")
def setAutoBrightness(payload):
    global autoBrightness
    autoBrightness = payload["autobrightness"]
    print("auto",autoBrightness)
    if autoBrightness == True:
        d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,6)
    else:
        pixels.brightness = 0.5
        socketio.emit("B2F_SetBrightness",{"brightness": pixels.brightness},broadcast=True)
        d = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),None,None,4,7)
    socketio.emit("B2F_autoBrightness",{"autobrightness": autoBrightness},broadcast=True)

@socketio.on("F2B_Shutdown")
def shutdown():
    print("shutdown")
    Shutdown_knop("f")

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def start_schakeling_thread():
    print("**** Starting SCHAKELING THREAD ****")
    schakelingThread = threading.Thread(target=codeSchakeling, args=(), daemon=True)
    schakelingThread.start()

def start_weight_thread():
    print("**** Starting WEIGHT THREAD ****")
    weightThread = threading.Thread(target=getWeight,args=(),daemon=True)
    weightThread.start()
    

def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')         
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()


# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        setup_gpio()
        start_schakeling_thread()
        start_weight_thread()
        # start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
        lcd.reset_lcd()
        pixels.deinit()
    finally:
        GPIO.cleanup()