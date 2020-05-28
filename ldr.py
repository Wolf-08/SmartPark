from RPi import GPIO
import random
import time
from flask import Flask
from threading import Thread
from DP1Database import Database
import datetime

app = Flask(__name__)

conn = Database(app=app, user='SPI', password='spi123',
                db='SEmbebidos', host='localhost',port=3306)

GPIO.setmode(GPIO.BCM)
TRIG = 20
ECHO = 21
value = 0
ldr = 18 #Pin del led 
led = 27
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)

running=False
distancia=0

"""
Se obtienen datos de la base y se encienden los sensores 
"""

class Encender(Thread):
    def __init__(self, mysqlcon):
        Thread.__init__(self)
        self.deamon = True
        self.conn = mysqlcon
        
        self.sensor_id_distance1 = self.conn.get_data('SELECT * FROM sensor WHERE sensornaam="distance1"')
        if not self.sensor_id_distance1:
            self.sensor_id_distance1 = self.conn.set_data('INSERT INTO sensor VALUES (NULL, "distance1", "cm" )')
        else:
            self.sensor_id_distance1 = int(self.sensor_id_distance1[0]['sensor_id'])

        self.sensor_id_ldr = self.conn.get_data('SELECT * FROM sensor WHERE sensornaam="ldr"')
        if not self.sensor_id_ldr:
            self.sensor_id_ldr = self.conn.set_data('INSERT INTO sensor VALUES (NULL, "ldr", NULL )')
        else:
            self.sensor_id_ldr = int(self.sensor_id_ldr[0]['sensor_id'])
        
        self.sensor_id_distance2= self.conn.get_data('SELECT * FROM sensor WHERE sensornaam="distance2"')
        if not self.sensor_id_distance2:
            self.sensor_id_distance2= self.conn.set_data('INSERT INTO sensor VALUES (NULL, "distance2", "cm")')
        else:
            self.sensor_id_distance2 = int(self.sensor_id_distance2[0]['sensor_id'])
            
        self.start()

def run():
    global running,distance
    valid=False
    autos=0
    while running:
        valid=random.random() <0.8
        if valid:
            distancia =random.uniform(0,10)
            if distancia < 4:
                autos += 1
                currnet_time = datetime.datetime.now()
                datum = str(currnet_time)[0:16]
                row_inserted_ldr = conn.set_data(
                "INSERT INTO historiek(date, value, sensor_id) VALUES (%s,%s,%s)",
                [datum, autos, 2])

        currnet_time = datetime.datetime.now()
        datum = str(currnet_time)[0:16]
        row_inserted_distance1 = conn.set_data(
        "INSERT INTO historiek(date, value, sensor_id) VALUES (%s,%s,%s)",
        [datum, distancia, 1])

        print("Measured Distance = %.1f cm" % distancia)
        time.sleep(30)
    
def start():
    global running
    if running:
        print("Sensor de Entrada ok")
        return
    running=True
    print("SENSOR ENCENDIDO")
    thread=Thread(target=run)
    thread.start()
        
def stop():
    global running
    running=false

    
if __name__=="__main__":
    start()
    sensor = Encender(conn)

