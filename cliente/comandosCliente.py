#JPGM clase para comandos de cliente
from globalconst import *
import encripcion

class comandosCliente(object):

    def __init__(self):
        pass

    def getTrama(self, comando, variable1, variable2 = "", separador = "$"):
       
        
        
        if(comando != ""):

            trama = bytes
            #MVFC se codifica la variable para poderla sumar
            variable1 = variable1.encode()
            separador = separador.encode()
            #puede venir 1, 2 o mas, yo voy a empezar a partir para armar la trama
            if(comando == COMMAND_FTR): #transferencia archivos, usa dos variables y una constante
                variable2 = variable2.encode()
                trama = comando + bytes(separador) + bytes(variable1) + bytes(separador) + bytes(variable2)
            elif(comando == COMMAND_ALIVE): #alive usa 1 variable y una constante
                trama = comando + bytes(separador) + bytes(variable1)
            elif(comando == COMMAND_CHAT): #comando para chat
                #se valida si esta activa la bandera de encripcion -- ya viene convertido a binario
                if(ENCRIPTARINFO == 1):
                    #se encripta el mensaje
                    print("esta encriptando")
                    variable1 = encripcion.encripcion().encriptar(variable1) 
                    trama = comando + bytes(separador) + variable1
                    print(trama)
                else:
                    #no se encripta el mensaje y se maneja como de costumbre
                    trama = comando + bytes(separador) + bytes(variable1)

            elif(comando == COMMAND_ACK): #comando para acknowledge
                trama = comando + bytes(separador) + bytes(variable1)
            elif(comando == COMMAND_FRR): #comando para FRR
            
                variable2 = variable2.encode()
        
                trama = comando + bytes(separador) + bytes(variable1) + bytes(separador) + bytes(variable2)
            return trama
        else: #es archivo de audio
            return variable1
            
            
        

    def splitTramaCliente(self, trama, separador = "$"):  
        trama = bytes(trama)
        trama = trama.decode()
        arregloTrama = trama.split(separador)

        #validacion de desencripcion
        #si es chat, se procede a desencriptar el mensaje si esta activa la bandera
        
        if(arregloTrama[0].encode() == COMMAND_CHAT and ENCRIPTARINFO == 1):
            #desencripto el mensaje y lo vuelvo a guardar en el arreglo
            print(arregloTrama[1])
            arregloTrama[1] = encripcion.encripcion().desencriptar(bytes(arregloTrama[1])).decode()
            
        
        return arregloTrama
        
            
#codigo de test clase
#objetoComandos = comandosCliente()
# # # # # trama_recibida = objetoComandos.getTrama(binascii.unhexlify("05"), "201504408")
# # # trama_chat = objetoComandos.getTrama(b'\x80', str("hola"))
# # # print("trama chat: " + str(trama_chat))
# tramaCLiente = objetoComandos.splitTramaCliente(b'\x08$hola', "$")
# # print(tramaCLiente)
# print(type(tramaCLiente[0].encode()))
# print(type(binascii.unhexlify("08")))
# print(type(binascii.unhexlify("04")))

# if(tramaCLiente[0].encode() != binascii.unhexlify("04")):
#     print("mensaje de texto")
#     print(tramaCLiente[0].encode())
# else:
#     print(tramaCLiente[0].encode())
# filesize = 64 * 1024
# tramaCLiente = objetoComandos.getTrama(binascii.unhexlify("03"), str("201504408"), str(filesize))
# print(tramaCLiente)
# tramasplit = objetoComandos.splitTramaCliente(tramaCLiente, "$")
# print(tramasplit)