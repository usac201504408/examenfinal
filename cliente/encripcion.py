
from Crypto.Cipher import AES
from globalconst import *


class encripcion(object):

    def __init__(self):
        pass

    def encriptar(self, mensaje):
        obj = AES.new(LLAVEAES, AES.MODE_CFB, IV_ENCRIPT)
        texto_encriptado = obj.encrypt(mensaje)
        return texto_encriptado

    def desencriptar(self, mensaje):
        obj2 = AES.new(LLAVEAES, AES.MODE_CFB, IV_ENCRIPT)
        texto_desencriptado = obj2.decrypt(mensaje)
        return texto_desencriptado

    def encriptarFile(self, archivo):
        obj = AES.new(LLAVEAES, AES.MODE_CFB, IV_ENCRIPT)
        # archivo = open("../cliente/tempFiles/recibido.wav", "rb")
        # bytesfile = archivo.readlines()
        with open("../cliente/tempFiles/enviar.wav", "rb") as archivo:
            todosbytes = archivo.read()
            texto_encriptado = obj.encrypt(todosbytes)
        
        archivo.close()

        with open("../cliente/tempFiles/enviarEncript.wav", "wb") as archivoencript:
            archivoencript.write(texto_encriptado)
        
        archivoencript.close()
        
        return texto_encriptado

    def desencriptarFile(self, archivo):
        obj = AES.new(LLAVEAES, AES.MODE_CFB, IV_ENCRIPT)
        # archivo = open("../cliente/tempFiles/recibido.wav", "rb")
        # bytesfile = archivo.readlines()       

        with open("../cliente/tempFiles/recibidoEncript.wav", "rb") as archivoencript:
            todosbytes = archivoencript.read()
            texto_desencriptado = obj.decrypt(todosbytes)
        
        archivoencript.close()


        with open("../cliente/tempFiles/recibidoDecript.wav", "wb") as archivo:
            archivo.write(texto_desencriptado)
        
        archivo.close()
        
        return texto_desencriptado

        
# encripcion().encriptarFile("")
# encripcion().desencriptarFile("")

# variable1 = "hola"    
# variable1 = variable1.encode()
# texto_encript = encripcion().encriptar(str(variable1.decode()))
# # # # print("texto encriptado")
# # print(texto_encript)
# # print(texto_encript)
# print(type(texto_encript))
# print(texto_encript.decode())

# arregloTrama = list()
# comandoByte = bytes(COMMAND_CHAT)
# # print(comandoByte)
# arregloTrama.append(COMMAND_CHAT)
# print(str(arregloTrama[0]))

# trama1 = b'\x08$\xe6@\xff\xc5'
# comando = trama1[:1]
# comando = bytes(comando)
# print(type(comando))


# trama = bytes(COMMAND_CHAT)
# trama = trama.decode()


# if(trama.encode() == COMMAND_CHAT):
#     print("es comando chat")
#     # print(comando.decode())

# # print(bytes(COMMAND_CHAT).decode())
# dataencriptada = trama1[2:]
# texto_decript = encripcion().desencriptar(dataencriptada)

# print(texto_decript.decode())


# # trama = bytes(str(trama).encode())
# # trama = trama.decode()
# arregloTrama = str(trama).split("$")
# texto_decript = encripcion().desencriptar(arregloTrama[0])
# print(texto_decript)


# trama = bytes(b'\x08$\xe6@\xff\xc5')
# print(trama)
# trama = trama.decode()
# arregloTrama = trama.split("$")

# texto_decript = encripcion().desencriptar(dataencriptada)
# # # # # print("dexto desencriptado")
# # # # print(texto_decript)
# # print(texto_decript)
# # print(type(texto_decript))
# print(texto_decript)




#codigo para generar nuevas llaves
# random_generator = Crypto.Random.new().read
# private_key = RSA.generate(1024, random_generator)
# public_key = private_key.publickey()
# private_key = private_key.exportKey(format='DER')
# public_key = public_key.exportKey(format='DER')
# private_key = binascii.hexlify(private_key).decode('utf8')
# public_key = binascii.hexlify(public_key).decode('utf8')
# print("Llave privada: "  + str(private_key))
# print("Llave publica: "  + str(public_key))




