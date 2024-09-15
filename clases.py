class Dato:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Pila:
    def __init__(self):
        self.cima = None
        self.size = 0

    def insertar(self, valor):
        nuevo = Dato(valor)
        if self.cima is None:
            self.cima = nuevo
        else:
            nuevo.siguiente = self.cima
            self.cima = nuevo
        self.size += 1
