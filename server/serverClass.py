import paho.mqtt.client as mqtt
from broker import *
from globalconst import *
import comandosCliente
import binascii
import logging
import threading
import time
import lecturaArchivos
import os
import alive
import servidorTCP


class clienteClass(object):

    def __init__(self, usuarioCliente):
        self.usuarioCliente = usuarioCliente
        pass

    def postAlive(self):
        while True:
            #hago un publish para decir que estoy vivo
            trama = comandosCliente.comandosCliente().getTrama(COMMAND_ALIVE, "201504408")       
            # client.publish("comandos/14/201504408", trama, qos = 2, retain = False)
            time.sleep(20)

    def negociacionRedireccion(self, destinatario, fileSize, nombreFile):
    
        if(str(destinatario).isdigit() == True): #es un carnet
            trama_redireccion = comandosCliente.comandosCliente().getTrama(COMMAND_FRR,destinatario,fileSize)
            #client.publish("comandos/14/" + str(destinatario), trama_redireccion, qos = 2, retain = False)
            self.publicar("comandos/14/" + str(destinatario), trama_redireccion)
            print("Enviando comando FRR al cliente destino " + str(destinatario) + " nombre archivo: " + str(nombreFile) + " de tamanio " + str(fileSize))
            #se empieza la transferencia
            pass
        else: #es una sala, tengo que enciclar hasta mandar a todos, revisando quienes estan en esa sala
            #con el archivo de listado de personas asignadas a salas
            usuariosRegistrados = lecturaArchivos.LecturaArchivo("usuarios.txt").getArreglo()
            for usuarioDestino in usuariosRegistrados:
                #recorro cada item del arreglo para ver si le toca recibir el archivo o no
                #verifico en todas las salas que tenga asignadas
                objetoUsuario = usuarioDestino.split(",") 
                carnetDestino = objetoUsuario[0]
                longitud = len(objetoUsuario)
                #si la longitud es mayor a dos, la persona esta asignada a alguna sala, si no no.
                if(longitud >= 2):
                    for index in range(2,longitud):
                        #voy verificando si la sala que tiene asignada es la destino
                        salaAsignada = objetoUsuario[index]
                        print("sala asignada de " + str(carnetDestino) + " es : " + str(salaAsignada))
                        if(salaAsignada == destinatario):
                            #si tiene asignada la sala, entonces le envio la trama        
                            trama_redireccion = comandosCliente.comandosCliente().getTrama(COMMAND_FRR,str(carnetDestino),fileSize)
                            #client.publish("comandos/14/" + str(carnetDestino), trama_redireccion, qos = 2, retain = False)
                            self.publicar("comandos/14/" + str(carnetDestino), trama_redireccion)
                            print("Enviando comando FRR al cliente destino " + str(carnetDestino) + " nombre archivo: " + str(nombreFile) + " de tamanio " + str(fileSize))
            print("termino de enviar a todos los usuarios en la sala")        

 

    #Handler en caso suceda la conexion con el broker MQTT
    def on_connect(self, client, userdata, flags, rc): 
        connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
        logging.debug(connectionText)
        self.t1 = threading.Thread(name = 'Hilo alive',
                                target = self.postAlive,
                                args = (()),
                                daemon = True
                            )
        self.t1.start()

    #Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self, client, userdata, msg):
        #Se muestra en pantalla informacion que ha llegado
        logging.debug("Ha llegado el mensaje al topic: " + str(msg.topic))
        mensajedecode =  msg.payload.decode()
        arregloTrama_split = comandosCliente.comandosCliente().splitTramaCliente(msg.payload)
    

        if(arregloTrama_split[0].encode() == binascii.unhexlify("04")): #alive no muestro al cliente
            print("")
            print("El cliente del topic " + str(msg.topic) + " da el comando ALIVE y dice soy: " + str(arregloTrama_split[1]))
            logging.debug("El contenido del mensaje es: " + str(mensajedecode))
            trama_ack = comandosCliente.comandosCliente().getTrama(COMMAND_ACK, str(arregloTrama_split[1])) 
            #client.publish("comandos/14/" + str(arregloTrama_split[1]), trama_ack, qos = 2, retain = False)
            self.publicar("comandos/14/" + str(arregloTrama_split[1]), trama_ack)
            #procedo a guardar a la lista de vivos al cliente
            remitente = str(msg.topic).split("/")[2]
            alive.alives().usuarioAlive(remitente)


        elif(arregloTrama_split[0].encode() == binascii.unhexlify("05")): #acknowledge del server
            # print("")
            # print("El cliente del topic " + str(msg.topic) + "da el comando ACK y dice: " + str(arregloTrama_split[1]))
            # logging.debug("El contenido del mensaje es: " + str(mensajedecode))
            pass
        elif(arregloTrama_split[0].encode() == binascii.unhexlify("03")): #trama FTR de cliente
            print("")
            print("El cliente del topic " + str(msg.topic) + " da el comando FTR para enviar a: " + str(arregloTrama_split[1]) + " el tamanio es de: " + str(arregloTrama_split[2]))
            logging.debug("El contenido del mensaje es: " + str(mensajedecode))
            #se procede a evaluar si le damos respuesta de NO o de OK
            #se extrae el remitente del topic    
            remitente = str(msg.topic).split("/")[2]
            trama_ok = comandosCliente.comandosCliente().getTrama(COMMAND_OK, str(remitente)) 
            # client.publish("comandos/14/" + str(remitente), trama_ok, qos = 2, retain = False)
            self.publicar("comandos/14/" + str(remitente), trama_ok)
            print("Se envio un comando OK al cliente " + str(remitente))
            #se procede a recibir el archivo del cliente MESSI
            NuevoServerTCP = servidorTCP.servidorTCP('localhost' , 9800, 65495,9801)
            NuevoServerTCP.recibirservidor()



            #luego de recibirlo procedo a hacer la negociacion con el destinatario, inicio un hilo
            nombreFile = "archivo.wav"
            destinatario = arregloTrama_split[1]
            tamanioFile =  arregloTrama_split[2]
            t2 = threading.Thread(name = 'Contador de 1 segundo',
                                target = self.negociacionRedireccion,
                                args = ((str(destinatario), str(tamanioFile), str(nombreFile))),
                                daemon = True
                            )
            t2.start()
            
      
        
       

    #Handler en caso se publique satisfactoriamente en el broker MQTT
    def on_publish(self, client, userdata, mid): 
        publishText = "Publicacion satisfactoria"
        logging.debug(publishText)    


    def conectarMQTT(self):
        self.client = mqtt.Client(clean_session=True) #JPGM Nueva instancia de cliente
        self.client.on_connect = self.on_connect #Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_message = self.on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.on_publish = self.on_publish #Se configura la funcion "Handler" que se activa al publicar algo
        self.client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
        

    def logginWriteInfo(self, mensaje):
        logging.info(mensaje)  

    def iniciarLoggin(self):
        logging.basicConfig(
        level = logging.INFO, 
        format = '\n \n [%(levelname)s]  %(message)s \n \n'
        )  
        

    def publicar(self, topic, trama):
        self.client.publish(topic, trama, qos = 2, retain = False)

    def suscribirse(self, topic,):
        self.client.subscribe((str(topic),  2))

    def iniciarLoop(self):
        #JPGM Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
        self.client.loop_start()

    def pararLoop(self):
        self.client.loop_stop()

    def desconectarBroker(self):
        self.client.disconnect()