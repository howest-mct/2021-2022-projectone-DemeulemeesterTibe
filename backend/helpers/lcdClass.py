from RPi import GPIO
import time
from smbus import SMBus
# Nog dingen aan toevoegen


class lcdClass:
    def __init__(self, RS, E, listDB=[], pcf=False) -> None:
        self.DBS = listDB
        self.RS = RS
        self.E = E
        self.teller = 0
        self.rij = 1
        self.pcf = pcf
        if self.pcf == True:
            self.i2c = SMBus()
            self.i2c.open(1)
        #
        self.setup()
        self.init_LCD()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
    
    def init_LCD(self):
        self.send_instruction(0b00111000)
        self.send_instruction(0b00001111)
        self.send_instruction(0b00000001)

    def send_instruction(self, value):
        GPIO.output(self.RS, GPIO.LOW)
        self.set_data_bits(value)
        GPIO.output(self.E, GPIO.HIGH)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.RS, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.E, GPIO.HIGH)
        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.01)

    def write_message(self, text):
        for char in text:
            self.teller += 1
            self.send_character(ord(char))
            # if(self.teller == 16):
            #     if(self.rij == 1):
            #         self.rij += 1
            #         self.second_row()
            #     elif(self.rij == 2):
            #         self.rij = 1
            #         self.first_row()
            #     self.teller = 0

    def set_data_bits(self, value):
        if self.pcf == False:
            mask = 0b00000001
            for i in range(0, 8):
                if (value & mask) > 0:
                    GPIO.output(self.DBS[i], GPIO.HIGH)
                else:
                    GPIO.output(self.DBS[i], GPIO.LOW)
                mask = mask << 1
        else:
            self.i2c.write_byte(0x20, value)
            # print(self.i2c.read_byte(0x20))

    def reset_lcd(self):
        self.send_instruction(0b00000001)

    def reset_cursor(self):
        self.send_instruction(0b00000010)

    def second_row(self):
        self.teller = 0
        self.send_instruction(0b10000000 | 0x40)

    def set_cursor(self, value):
        self.send_instruction(0b10000000 | value)

    def first_row(self):
        self.teller = 0
        self.send_instruction(0b10000000)

    def move_screen_right(self):
        self.send_instruction(0b00011000)

    def move_screen_left(self):
        self.send_instruction(0b00011100)