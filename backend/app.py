import time
from RPi import GPIO
from helpers.lcdClass import lcdClass
from helpers.klasseknop import Button
from helpers.spiclass import SpiClass
from hx711 import HX711
from datetime import datetime
import threading
from subprocess import check_output
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository

from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# variabelen
dtWeight = 6
clkWeight = 13

alarmopScherm = True
rs = 21
e =  20
buzz = 26
buzzer = ""
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
alarm = ""
aan = False
timer = 0
timerldr = time.time()
# objecten
joyBtn = Button(19)
btn = Button(12)
spi = SpiClass(0,0)
lcd = lcdClass(rs,e,None,True)
# hx = HX711(dtWeight,clkWeight)

# Code voor Hardware
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz, GPIO.OUT)
    buzzer = GPIO.PWM(buzz,440)
    buzzer.start(0)
    btn.on_press(lees_knop)
    joyBtn.on_press(joy_knop)

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

def codeSchakeling():
    global minldr,maxldr,aan,timer,timerldr
    while True:
        timer = time.time()
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
            lichtsterkte = round(100 - (100*((waardeldr - minldr) / (maxldr - minldr))),2)
            # print(f"Lichtsterkte: {lichtsterkte:.2f} %")
        if timer - timerldr >= 60:
            print("LDR inlezen") 
            timerldr = time.time()
            # insert = DataRepository.insert_historiek(time.strftime('%Y-%m-%d %H:%M:%S'),lichtsterkte,None,2,1)
            # print(insert)
            # data = DataRepository.read_historiek_by_id(insert)
            # print(data)
            # socketio.emit('B2F_verandering_ldr', {'ldr': data}, broadcast=True)
        # alarm 
        if huidigetijd == alarm:
            aan = True
        if aan == True:
            print("buzzen")

def displayStatus(lcdStatus,y,x):
    global vorips , tijd , teller , joyTimer , alarmopScherm, huidigetijd,timer
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
    elif lcdStatus == 2:
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
            alarmopScherm = False
            
    elif lcdStatus == 3:
        
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
        data = DataRepository.insert_alarm(gegevens["naam"],gegevens["tijd"])
        return jsonify(alarmid=data),201
            



@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    # status = DataRepository.read_status_lampen()
    # emit('B2F_status_lampen', {'lampen': status}, broadcast=True)

    data = DataRepository.read_historiek_by_id(20)
    socketio.emit("B2F_verandering_ldr",{'ldr': data}, broadcast=True)

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=codeSchakeling, args=(), daemon=True)
    thread.start()


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
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        lcd.reset_lcd()
        GPIO.cleanup()

