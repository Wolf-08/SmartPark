import time
from RPi import GPIO
from flask import Flask, jsonify, request ,render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from DP1Database import Database
import ldr
import rfidreader
from LCD import LCD_run
import  parkingSensor
import pigpio

app = Flask(__name__)
CORS(app)
#Conexion a la base de Datos
conn = Database(app=app, user='SPI', password='spi123',
                db='SEmbebidos', host='localhost',port = 3306)


#Se llama la clase que inicia el LCD
LCD_run()

# Se enciende los leds fotoresistentes con la llegada de autos. 
luz= ldr.Encender(conn)
ldr.start()

#Iniciamos el sensor del estacionamiento
parkingSensor.start()

servoPIN = 17

#Indicamos en que modo se usan  los pines de las raspberry
#BCM es para referirnos por su nombre GPIO y no como estan impresos
GPIO.setmode(GPIO.BCM)
#Accede a los gpio de la rasp
piGPIO = pigpio.pi()
total = 6
#Pines y frecuencia 
#piGPIO.set_PWM_frequency(servoPIN, 50)
#piGPIO.set_PWM_dutycycle(servoPIN, (7.5 / 100) * 255)
#GPIO.setwarnings(False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parking")
def parking():
    return render_template("parking.html",
    distancia=float(parkingSensor.distancia))


@app.route("/acceder")
def acceso():
    return render_template("access.html"
    ,autos=int(ldr.autos),
    total=total)
# refers to the class that works the rfid reader and the automatic barrier


Barrera = rfidreader.rfid(conn, openSlagboom)

app.run(port="80")
