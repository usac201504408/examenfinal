#socket.sendfile() disponible desde Python 3.3

import socket
import time

class servidorTCP(): #creamos una clase para el servidor
    def __init__(self,a,p,b,p1): #definimos las variables iniciales a utilizar
        self.addr = a
        self.port = p
        self.port1 = p1
        self.buff = b #8 KB para buffer de transferencia de archivos
        # self.server_socket = socket.socket() 
        # self.server_socket.bind(('localhost', self.port1))
        # self.server_socket.listen(10) #1 conexion activa y 9 en cola
        # self.server_socket.setblocking(False)
        

    


    def mandarservidor(self): #metodo para mandar un archivo de audio servidor
        server_socket = socket.socket() 
        server_socket.bind((self.addr, self.port1))
        server_socket.listen(10) #1 conexion activa y 9 en cola
        try:
            #while True:
                # self.server_socket.listen(100)
                print("\nEsperando conexion remota...\n")
                conn, addr = server_socket.accept()
                print('Conexion establecida desde ', addr)
                print('Enviando archivo de audio')
                with open('../server/tempFiles/recibido.wav', 'rb') as f: #Se abre el archivo a enviar en BINARIO
                    conn.sendfile(f, 0)
                    f.close()
                conn.close()
                print("\n\nArchivo enviado a: ", addr)
        except Exception as exp:
            print("Ocurrio un error...:" + str(exp))
        finally:
            print("Cerrando servidor...")
            #seeever_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
            # conn.close()
            #self.server_socket.detach()

    def recibirservidor(self): #se crea un metodo para recibir un audio en el servidor
        server_socket = socket.socket()
        server_socket.bind((self.addr, self.port1))
        server_socket.listen(10) #1 conexion activa y 9 en cola
        try:
            #while True:
                server_socket.listen(100)
                print("\nEsperando conexion remota...\n")
                conn, addr = server_socket.accept()
                print('Conexion establecida desde ', addr)
                print('recibiendo audio de cliente...')
                buff=self.buff
                with open('../server/tempFiles/recibido.wav', 'wb') as f: #Se abre el archivo a enviar en BINARIO
                    while buff:
                        buff = conn.recv(self.buff)
                        f.write(buff)
                    f.close()
                conn.close()
                print("\n\n recibido audio de: ", addr)
        except Exception as ex:
            print("Ocurrio un error...: " + str(ex))
        finally:
            print("Cerrando servidor...")        
            #server_socket.shutdown()
            #self.server_socket.listen(100)
            server_socket.close()
            # conn.close()
            #self.server_socket.detach()

    def inicializarServerSocket(self):
        pass

    def desconectarSocket(self):
        # server_socket.close()
        pass
        

# Datos= servidorTCP('localhost' , 9800, 65495,9801) #Definimos los valores iniciales
# Datos.mandarservidor()
# Datos.recibirservidor()