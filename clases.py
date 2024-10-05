class Producto:
    def __init__(self, nombre, elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion
        self.siguiente = None

    def __str__(self):
        return f"Nombre: {self.nombre}, Elaboración: {self.elaboracion}"

class Maquina:
    def __init__(self, nombre, produccion, componentes, tiempo, pila_productos):
        self.nombre = nombre
        self.produccion = produccion
        self.componentes = componentes
        self.tiempo = tiempo
        self.pila_productos = pila_productos
        self.siguiente = None

    def __str__(self):
        return f"Nombre: {self.nombre}, Producción: {self.produccion}, Componentes: {self.componentes}, Tiempo: {self.tiempo}"

class Instruccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

    def __str__(self):
        return f"Instrucción: {self.nombre}"

from abc import ABC, abstractmethod

class Pila(ABC):
    def __init__(self):
        self.primero = None
        self.size = 0

    @abstractmethod
    def insertar(self):
        pass

    def buscar(self, nombre):
        actual = self.primero
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

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

    def getProducto(self, nombre_producto):
        # Buscar el producto con el nombre dado
        producto = self.buscar(nombre_producto)
        if producto is None:
            return None

        return producto

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

    def getMaquina(self, nombre_maquina):
        # Buscar la máquina con el nombre dado
        maquina = self.buscar(nombre_maquina)
        if maquina is None:
            return None

        return maquina

    def getProductos(self, nombre_maquina):
        # Buscar la máquina con el nombre dado
        maquina = self.buscar(nombre_maquina)
        if maquina is None:
            return PilaProductos()

        # Obtener los nombres de los productos de la máquina
        nombres_productos = maquina.pila_productos.getNames()

        # Dividir la cadena de nombres de productos en cada coma
        lista_productos = nombres_productos.split(",")

        return lista_productos
    
class PilaInstrucciones(Pila):
    def insertar(self, instruccion):
        nuevo_nodo = Instruccion(instruccion)
        nuevo_nodo.siguiente = self.primero
        self.primero = nuevo_nodo
        self.size += 1

    def print(self):
        for instruccion in self:
            print(f"Instrucción: {instruccion.instruccion}")

    def getInstruccion(self, instruccion):
        # Buscar la instrucción con el nombre dado
        instruccion = self.buscar(instruccion)
        if instruccion is None:
            return None

        return instruccion