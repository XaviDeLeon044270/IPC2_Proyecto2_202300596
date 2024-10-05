from flask import Flask, render_template, request, flash, redirect, url_for, session
import os
import xml.etree.ElementTree as ET
from clases import PilaMaquinas, PilaProductos, PilaInstrucciones
from graphviz import Digraph
from jinja2 import Environment, FileSystemLoader

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'alguna clave secreta única y secreta'
        self.pila_maquinas = PilaMaquinas()
        self.pila_productos = PilaProductos()
        self.pila_instrucciones = PilaInstrucciones()

        self.app.jinja_env.globals.update(zip=zip, abs=abs)

        self.app.route('/')(self.home)
        self.app.route('/archivo', methods=['GET', 'POST'])(self.archivo)
        self.app.route('/tabla')(self.tabla)
        self.app.route('/info')(self.info)
        self.app.route('/reportes')(self.reportes)

    def home(self):
        return render_template('index.html')

    def archivo(self):
        if request.method == 'POST':
            # Obtenemos la máquina seleccionada
            maquina_seleccionada = request.form.get('maquina')

            # Obtenemos el producto seleccionado
            producto_seleccionado = request.form.get('producto')

            # Almacenamos la máquina seleccionada en la sesión
            session['maquina_seleccionada'] = maquina_seleccionada
            # Almacenamos el producto seleccionado en la sesión
            session['producto_seleccionado'] = producto_seleccionado

            print(f"Producto seleccionado: {producto_seleccionado}")

            if 'fileInput' not in request.files:
                return redirect(url_for('archivo', maquina_seleccionada=maquina_seleccionada))

            file = request.files['fileInput']
            if file.filename == '':
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

    def tabla(self):
        # Obtenemos el producto y la máquina seleccionados de la sesión
        print("Se entró a la tabla")
        producto_seleccionado = session.get('producto_seleccionado')
        maquina_seleccionada = session.get('maquina_seleccionada')

        # Obtenemos los objetos de la máquina y el producto
        maquina = self.pila_maquinas.getMaquina(maquina_seleccionada)

        if maquina is None:
            print("No se encontró la máquina seleccionada")
            return render_template('tabla.html', maquina=None)

        producto = maquina.pila_productos.getProducto(producto_seleccionado)

        if producto is None:
            print("No se encontró el producto seleccionado")
            return render_template('tabla.html', maquina=maquina)

        # Imprimimos los atributos de la máquina y el producto seleccionados
        print(f"Máquina seleccionada: {maquina}")
        print(f"Producto seleccionado: {producto}")

        # Limpiamos la pila de instrucciones
        self.pila_instrucciones.clear()

        # Obtenemos las instrucciones del producto
        for instruccion in producto.elaboracion.split():
            print(f"Procesando instrucción: {instruccion}")  # Agrega esta línea
            
            linea = int(instruccion[1])
            componente = int(instruccion[3])
            self.pila_instrucciones.insertar(linea, componente)
            print(f"Instrucción: L{linea} C{componente}")

        # Pasamos los datos a la plantilla
        return render_template('tabla.html', maquina=maquina, producto=producto, instrucciones=self.pila_instrucciones)

    def reportes(self):
        # Obtenemos el producto y la máquina seleccionados de la sesión
        print("Se entró a la tabla")
        producto_seleccionado = session.get('producto_seleccionado')
        maquina_seleccionada = session.get('maquina_seleccionada')

        # Obtenemos los objetos de la máquina y el producto
        maquina = self.pila_maquinas.getMaquina(maquina_seleccionada)

        if maquina is None:
            print("No se encontró la máquina seleccionada")
            return render_template('error.html', mensaje="No se encontró la máquina seleccionada")

        producto = maquina.pila_productos.getProducto(producto_seleccionado)

        if producto is None:
            print("No se encontró el producto seleccionado")
            return render_template('error.html', mensaje="No se encontró el producto seleccionado")

        # Imprimimos los atributos de la máquina y el producto seleccionados
        print(f"Máquina seleccionada: {maquina}")
        print(f"Producto seleccionado: {producto}")

        # Limpiamos la pila de instrucciones
        self.pila_instrucciones.clear()

        # Creamos un gráfico de Graphviz
        g = Digraph('G', filename='reporte.gv')

        # Obtenemos las instrucciones del producto
        for instruccion in producto.elaboracion.split():
            print(f"Procesando instrucción: {instruccion}")  # Agrega esta línea
            
            linea = int(instruccion[1])
            componente = int(instruccion[3])
            self.pila_instrucciones.insertar(linea, componente)
            print(f"Instrucción: L{linea} C{componente}")

            # Agregamos los nodos y las aristas al gráfico
            g.node(f"L{linea} C{componente}")
            if instruccion != producto.elaboracion.split()[0]:
                g.edge(f"L{linea_anterior} C{componente_anterior}", f"L{linea} C{componente}")

            linea_anterior = linea
            componente_anterior = componente

        # Generamos el gráfico y lo guardamos como una imagen PNG
        g.format = 'png'
        g.render(filename='static/reporte', cleanup=True)

        return render_template('reportes.html')
    
    def info(self):
        return render_template('info.html')

    def run(self):
        self.app.run(host='localhost', debug=True)


if __name__ == '__main__':
    app = MyApp()
    app.run()