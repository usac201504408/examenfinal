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
import clienteTCP


class clienteClass(object):

    def __init__(self, usuarioCliente, esperandoRespuesta):
        self.usuarioCliente = usuarioCliente
        self.esperandoRespuesta = esperandoRespuesta
        pass

    def postAlive(self):
        while True:
            #JPGM hago un publish para decir que estoy vivo
            trama = comandosCliente.comandosCliente().getTrama(COMMAND_ALIVE, self.usuarioCliente)       
            self.client.publish("comandos/14/" + str(self.usuarioCliente), trama, qos = 2, retain = False)
            time.sleep(ALIVE_PERIOD)

    def hiloAudio(self):
        #JPGM el archivo de audio se sobreescribe en el mismo archivo cada vez que se recibe
        try:
            os.system('aplay ../cliente/tempFiles/recibido.wav')
        except Exception as ex:
            print("error: " + ex)



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
        #JPGM Se muestra en pantalla informacion que ha llegado
        # print(msg.payload)
        # print("llego")
        # print(msg.payload)
        # print(type(msg.payload))

        #obtener que topic es
        splitTopic = str(msg.topic).split("/")
        # print(splitTopic)
        topicBase = splitTopic[0]

        if(topicBase != "audio"):
                
            arregloTrama_split = comandosCliente.comandosCliente().splitTramaCliente(msg.payload)
            # print(arregloTrama_split)
            
            if(arregloTrama_split[0].encode() == COMMAND_ALIVE): #alive no muestro al cliente
                pass
            elif(arregloTrama_split[0].encode() == COMMAND_ACK): #acknowledge del server
                # print("")
                # print("El cliente del topic " + str(msg.topic) + " da el comando ACK y dice: " + str(arregloTrama_split[1]))
                # logging.debug("El contenido del mensaje es: " + str(mensajedecode))
                pass
            elif(arregloTrama_split[0].encode() == COMMAND_FTR): #trama FTR del ciente      
                pass
            elif(arregloTrama_split[0].encode() == COMMAND_OK): #trama OK del server
                #bajo bandera de espera
                self.esperandoRespuesta
                self.esperandoRespuesta = False    
                pass
            elif (arregloTrama_split[0].encode() == COMMAND_CHAT):
                logging.info("El cliente del topic " + str(msg.topic) + " da el comando CHAT y dice: " + str(arregloTrama_split[1]))
               
            elif (arregloTrama_split[0].encode() == COMMAND_FRR): #trama FRR file receive request
                #conectarme al socket para recibir archivo MESSI
                # print("Cliente conectandose a SOCKET para recibir archivo ")
                print("empieza a recibir audio")
                NuevoClienteTCP = clienteTCP.clienteTCP(IP_TCP , 9800, 65495,TCP_PORT)
                NuevoClienteTCP.recibircliente()    
                 
                self.t2 = threading.Thread(name = 'Hilo audio',
                                       target = self.hiloAudio,
                                       args = (()),
                                       daemon = False
                                   )
                self.t2.start()
        else:#es audio por mqtt

            #guardo el archivo y luego llamo al hilo
            nombreArchivo = "../cliente/tempFiles/recibido.wav"
            out_file = open(nombreArchivo, "wb") # open for [w]riting as [b]inary
            out_file.write(msg.payload)
            out_file.close()

            self.t2 = threading.Thread(name = 'Hilo audio',
                                target = self.hiloAudio,
                                args = (()),
                                daemon = False
                            )
            self.t2.start()
            
      
        
       

             

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

