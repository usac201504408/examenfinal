#JPGM clase para comandos de cliente
from globalconst import *

class comandosCliente(object):

    def __init__(self):
        pass

    def getTrama(self, comando, variable1, variable2 = "", separador = "$"):
       
        trama = bytes
        
        
        #se codifica la variable para poderla sumar
        variable1 = variable1.encode()
        separador = separador.encode()
        #puede venir 1, 2 o mas, yo voy a empezar a partir para armar la trama
        if(comando == COMMAND_FTR): #transferencia archivos, usa dos variables y una constante
            pass
        elif(comando == COMMAND_ALIVE): #alive usa 1 variable y una constante
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == COMMAND_CHAT): #comando para chat
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == COMMAND_ACK): #comando para acknowledge
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == COMMAND_OK): #comando para OK
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == COMMAND_NO): #comando para NO
            trama = comando + bytes(separador) + bytes(variable1)
        elif(comando == COMMAND_FRR): #comando para FRR
            variable2 = variable2.encode()
            trama = comando + bytes(separador) + bytes(variable1) + bytes(separador) + bytes(variable2)
            
            
        return trama

    def splitTramaCliente(self, trama, separador = "$"):
        #verifico si le muestro o no al usuario este mensaje
        #las tramas ALIVE emitidas por el cliente no se las muestro a el
        trama = bytes(trama)
        trama = trama.decode()
        arregloTrama = trama.split(separador)
        
        return arregloTrama
        
            
#codigo de test clase
# objetoComandos = comandosCliente()
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