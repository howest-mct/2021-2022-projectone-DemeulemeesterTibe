import time
from RPi import GPIO
import sys
buzz = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz, GPIO.OUT)
buzzer = GPIO.PWM(buzz,1000)
buzzer.start(10)
try:
    while True:
        buzzer.ChangeFrequency(440)
        time.sleep(1)
        buzzer.ChangeFrequency(784)
        time.sleep(1)

except KeyboardInterrupt:
    print("KBDSFOIHDSFGHUIOLUQGFGUFIDUGHIFDS")
finally:
    GPIO.cleanup()