import serverClass
import lecturaArchivos
import comandosCliente
from broker import *
from globalconst import *
import os

#variables globales:
qos = 2
usuarioCarnet = "" #NUMERO DE CARNET DEL CLIENTE

#se instancia la clase
serverMain = serverClass.serverClass(usuarioCarnet)
serverMain.conectarMQTT()
serverMain.iniciarLoggin()
serverMain.conectarSocket()


#suscribirse a todos los topics del archivo
topics = lecturaArchivos.LecturaArchivo("topics.txt").getArreglo()

for topic in topics:
    serverMain.suscribirse(topic)

serverMain.iniciarLoop()


#El thread de MQTT queda en el fondo, mientras en el main loop hacemos otra cosa
try:
    while True:
        pass


except KeyboardInterrupt:
    serverMain.logginWriteInfo("Desconectando del broker...")

finally:
    serverMain.pararLoop() #Se mata el hilo que verifica los topics en el fondo
    serverMain.desconectarBroker() #Se desconecta del broker
    # logging.info("Desconectado del broker. Saliendo..
    serverMain.desconectarSocket()
    serverMain.logginWriteInfo("Desconectado del broker. Saliendo...")
    # print("Desconectado del broker. Saliendo...")