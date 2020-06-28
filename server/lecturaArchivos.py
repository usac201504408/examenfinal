#clase para lectura de archivos


class LecturaArchivo(object):

    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo

    def getArreglo(self):
        datos = list()
        archivo = open(self.nombreArchivo, 'r')
        for linea in archivo:
            datos.append(linea.replace('\n', '').strip())
        archivo.close()
        return datos

    def escribirArreglo(self, valor):
        archivo = open(self.nombreArchivo, 'a')
        textoAppend = str(valor) + "\n"
        archivo.write(textoAppend)
        archivo.close()

    def limpiarArchivo(self):
        archivo = open(self.nombreArchivo, 'w')
        archivo.write("")
        archivo.close()


#Ejemplo de consumo de la clase
# nuevoarreglo = LecturaArchivo("alives.txt")
# nuevoarreglo.limpiarArchivo()
# print(nuevoarreglo)
     

