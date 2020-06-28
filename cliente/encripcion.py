
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from globalconst import *


class encripcion(object):

    def __init__(self):
        pass

    def encriptar(self, mensaje):
        #volviendo a codificar los objetos de llave
        #CAMBIAR EL TIPO DE CIFRADO QUE TRAE CARACTER $ QUE USAMOS COMO SEPARADOR
        print(mensaje)
        private_key = RSA.importKey(binascii.unhexlify(PRIVATE_KEY))
        public_key = private_key.publickey()
        public_key = RSA.importKey(binascii.unhexlify(PUBLIC_KEY))
        cipher = PKCS1_OAEP.new(public_key)
        mensaje_encript  = cipher.encrypt(mensaje)
        return mensaje_encript

    def desencriptar(self, mensaje):
        #volviendo a codificar los objetos de llave
        #CAMBIAR EL TIPO DE CIFRADO QUE TRAE CARACTER $ QUE USAMOS COMO SEPARADOR
        private_key = RSA.importKey(binascii.unhexlify(PRIVATE_KEY))
        cipher = PKCS1_OAEP.new(private_key)
        mensaje_encript  = cipher.decrypt(mensaje)
        print(mensaje_encript)
        return mensaje_encript
    

# mensaje = "Hola mundo, soy un mensaje en texto plano, todo el mundo puede leerme."
# mensaje = mensaje.encode()
# texto_encript = encripcion().encriptar(mensaje)
# # print("texto encriptado")
# print(texto_encript)

# texto_decript = encripcion().desencriptar(texto_encript)
# # print("dexto desencriptado")
# print(texto_decript.decode())




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




