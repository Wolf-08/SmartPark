import RPi.GPIO as GPIO
import time
import random
import datetime
from threading import Thread
from flask import Flask
from DP1Database import Database

app = Flask(__name__)
conn = Database(app=app, user='SPI', password='spi123',
                db='SEmbebidos', host='localhost', port=3306)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 5
ECHO = 26
#Valores del sensor --Distancia para saber si esta ocupado o no el lugar
distancia=0
ocupadoV_buff=[]
ocupadoF_buuf=[]
valid=False
ocupado=False
running=False
#GPIO.setup(TRIG, GPIO.OUT)
#GPIO.setup(ECHO, GPIO.IN)
def run():
    global valid,ocupado, distancia,ocupado
    while running:
        valid= random.random() < 0.9
        if valid:
            distancia=random.uniform(0,10)
            if distancia <= 6:
                ocupado=True
                #1 ocupado
                current_time = datetime.datetime.now()
                datum = str(current_time)[0:16]
                conn.set_data(
                "INSERT INTO historiek(date, value, sensor_id) VALUES (%s,%s,%s)",
                [datum, 1, 3])
                
            else:
                ocupado=False
                #0  desocupado
                current_time = datetime.datetime.now()
                datum = str(current_time)[0:16]
                conn.set_data(
                "INSERT INTO historiek(date, value, sensor_id) VALUES (%s,%s,%s)",
                [datum, 0, 3])
    
   
            print("DISTANCIA CM : D={:.2f} V={}".format(distancia,valid))
            time.sleep(20)
def start():
    global running
    if running:
        print("Sensor Funcionando")
        return
    running=True
    print("Iniciando...")
    thread=Thread(target=run)
    thread.start()
def stop():
    global running
    running=False
    
if __name__=="__main__":
    start()
