import RPi.GPIO as GPIO
import sys
import time
from threading import Thread
from mfrc522 import SimpleMFRC522
import pigpio

# Initialization


class rfid(Thread):
    def __init__(self, mysqlcon, callback):
        self.servoPIN = 17
        GPIO.setmode(GPIO.BCM)
        self.callback = callback
        
        Thread.__init__(self)
        self.deamon = True
        self.conn = mysqlcon
        self.reader = SimpleMFRC522()

        
        self.piGPIO = pigpio.pi()
        self.piGPIO.set_PWM_frequency(self.servoPIN, 50)
        self.piGPIO.set_PWM_dutycycle(self.servoPIN, (7.5/100)*255)

        self.start()

    def run(self):
        while True:
            print("Sostenga la tarjeta cerca del lector")

            id, text = self.reader.read()
            print(id)
            print(text)

            isGood = self.conn.get_data("SELECT * FROM SEmbebidos.RFID WHERE SEmbebidos.RFID.adress = %s;", id)

            if isGood:
                print("open")
                self.callback()
                print("stopped")
            else:
                print("sorry")
                time.sleep(3)
