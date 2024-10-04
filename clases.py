class Producto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.siguiente = None

class Maquina:
    def __init__(self, nombre, produccion, componentes, tiempo, pila_productos):
        self.nombre = nombre
        self.produccion = produccion
        self.componentes = componentes
        self.tiempo = tiempo
        self.pila_productos = pila_productos
        self.siguiente = None


from abc import ABC, abstractmethod

class Pila(ABC):
    def __init__(self):
        self.primero = None
        self.size = 0

    @abstractmethod
    def insertar(self):
        pass

    def getNames(self):
        actual = self.primero
        nombres = ""
        while actual is not None:
            nombres += actual.nombre + ","
            actual = actual.siguiente
        return nombres.rstrip(",") 
    
    def clear(self):
        self.primero = None
        self.size = 0

    @abstractmethod
    def print(self):
        pass

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual
            actual = actual.siguiente

class PilaProductos(Pila):
    def insertar(self, nombre, elaboracion):
        nuevo_nodo = Producto(nombre, elaboracion)
        nuevo_nodo.siguiente = self.primero
        self.primero = nuevo_nodo
        self.size += 1

    def print(self):
        for producto in self:
            print(f"Nombre: {producto.nombre}")
            print(f"Elaboración: {producto.elaboracion}")

class PilaMaquinas(Pila):
    def insertar(self, nombre, produccion, componentes, tiempo, pila_productos):
        nuevo_nodo = Maquina(nombre, produccion, componentes, tiempo, pila_productos)
        nuevo_nodo.siguiente = self.primero
        self.primero = nuevo_nodo
        self.size += 1

    def print(self):
        for maquina in self:
            print(f"Nombre: {maquina.nombre}")
            print(f"Producción: {maquina.produccion}")
            print(f"Componentes: {maquina.componentes}")
            print(f"Tiempo: {maquina.tiempo}")
            print("Productos:")
            for producto in maquina.pila_productos:
                print(f"\tNombre: {producto.nombre}")
                print(f"\tElaboración: {producto.elaboracion}")

    def getProductos(self, nombre_maquina):
        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.nombre == nombre_maquina:
                return nodo_actual.pila_productos
            nodo_actual = nodo_actual.siguiente
        return None