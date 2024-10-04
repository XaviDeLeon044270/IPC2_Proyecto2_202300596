from flask import Flask, render_template, request, flash, redirect, url_for
import os
import xml.etree.ElementTree as ET
from clases import PilaMaquinas, PilaProductos

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'alguna clave secreta única y secreta'
        self.pila_maquinas = PilaMaquinas()
        self.pila_productos = PilaProductos()

        self.app.route('/')(self.home)
        self.app.route('/archivo', methods=['GET', 'POST'])(self.archivo)
        self.app.route('/info')(self.info)
        self.app.route('/reportes')(self.reportes)

    def home(self):
        return render_template('index.html')

    def archivo(self):
        if request.method == 'POST':
            # Obtenemos la máquina seleccionada
            maquina_seleccionada = request.form.get('maquina')

            # Buscamos la máquina en la pila de máquinas
            maquina = self.pila_maquinas.buscar(maquina_seleccionada)

            # Imprimimos los atributos de la máquina
            if maquina is not None:
                print("Nombre de la máquina:", maquina.nombre)
                print("Cantidad de líneas de producción:", maquina.produccion)
                print("Cantidad de componentes:", maquina.componentes)
                print("Tiempo de ensamblaje:", maquina.tiempo)
                print("Productos:", maquina.pila_productos.getNames())
            else:
                print("No se encontró la máquina:", maquina_seleccionada)

            if 'fileInput' not in request.files:
                flash("No se encontró el archivo")
                return redirect(url_for('archivo', maquina_seleccionada=maquina_seleccionada))

            file = request.files['fileInput']
            if file.filename == '':
                flash("No se seleccionó ningún archivo")
                return redirect(url_for('archivo', maquina_seleccionada=maquina_seleccionada))
            
            if file:
                tree = ET.parse(file)
                root = tree.getroot()

                # Limpiamos la pila de máquinas
                self.pila_maquinas.clear()

                for child in root.findall('Maquina'):
                    # Creamos una nueva pila de productos para la nueva máquina
                    pila_productos = PilaProductos()

                    nombreMaquina = child.find('NombreMaquina').text
                    produccion = int(child.find('CantidadLineasProduccion').text)
                    componentes = int(child.find('CantidadComponentes').text)
                    tiempo = int(child.find('TiempoEnsamblaje').text)

                    # Ahora buscamos los productos dentro de la máquina
                    productos = child.find('ListadoProductos')
                    if productos is not None:
                        for producto in productos.findall('Producto'):
                            nombreProducto = producto.find('nombre').text
                            elaboracion = producto.find('elaboracion').text

                            # Insertamos el producto en la pila de productos
                            pila_productos.insertar(nombreProducto, elaboracion)

                    # Insertamos la máquina en la pila de máquinas
                    self.pila_maquinas.insertar(nombreMaquina, produccion, componentes, tiempo, pila_productos)

                # Imprimir para depurar
                print("Maquinas:")
                self.pila_maquinas.print()

                flash("Archivo cargado con éxito")
                return redirect(url_for('archivo', maquina_seleccionada=maquina_seleccionada))
        else:
            # Obtenemos los nombres de las máquinas de la pila
            maquinas = self.pila_maquinas.getNames().split(",")
            maquina_seleccionada = request.args.get('maquina_seleccionada', default=None, type=None)

            # Obtenemos los productos de la máquina seleccionada
            productos = self.pila_maquinas.getProductos(maquina_seleccionada) if maquina_seleccionada else PilaProductos()

            # Pasamos los productos a la plantilla
            return render_template('archivo.html', maquinas=maquinas, productos=productos, maquina_seleccionada=maquina_seleccionada)

    def info(self):
        return render_template('info.html')

    def reportes(self):
        return render_template('reportes.html')

    def run(self):
        self.app.run(host='localhost', debug=True)


if __name__ == '__main__':
    app = MyApp()
    app.run()