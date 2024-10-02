class NodoMaquina:
    def __init__(self, nombre, produccion, componentes, tiempo):
        self.nombre = nombre
        self.produccion = produccion
        self.componentes = componentes
        self.tiempo = tiempo
        self.siguiente = None

class NodoProducto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.siguiente = None


class Pila:
    def __init__(self):
        self.primero = None
        self.size = 0

    def insertMachine(self, nombre, produccion, componentes=None, tiempo=None):
        nuevo = NodoMaquina(nombre, produccion, componentes, tiempo)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.size += 1

    def insertProduct(self, nombre, elaboracion):
        nuevo = NodoProducto(nombre, elaboracion)
        if self.primero is None:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.size += 1

    def printMachine(self):
        actual = self.primero
        while actual is not None:
            print(f"Nombre: {actual.nombre}, Producción: {actual.produccion}, Componentes: {actual.componentes}, Tiempo: {actual.tiempo}")
            actual = actual.siguiente

    def printProduct(self):
        actual = self.primero
        while actual is not None:
            print(f"Nombre: {actual.nombre}, Elaboración: {actual.elaboracion}")
            actual = actual.siguiente

    def printObject(self):
        actual = self.primero
        while actual is not None:
            print(actual.nombre)
            actual = actual.siguiente

    # Añadir el método __iter__
    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual
            actual = actual.siguiente
