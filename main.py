from flask import Flask, render_template, request, flash, redirect, url_for, session
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
            if 'fileInput' not in request.files:
                flash("No se encontró el archivo")
                return redirect(url_for('archivo'))

            file = request.files['fileInput']
            if file.filename == '':
                flash("No se seleccionó ningún archivo")
                return redirect(url_for('archivo'))
            
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
                return redirect(url_for('archivo'))
        else:
            # Obtenemos los nombres de las máquinas de la pila
            maquinas = self.pila_maquinas.getNames().split(",")
            maquina_seleccionada = request.form.get('maquina')
            productos = self.pila_maquinas.getProductos(maquina_seleccionada).split(",") if maquina_seleccionada else []
            return render_template('archivo.html', maquinas=maquinas, productos=productos)

    def info(self):
        return render_template('info.html')

    def reportes(self):
        return render_template('reportes.html')

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    app = MyApp()
    app.run()