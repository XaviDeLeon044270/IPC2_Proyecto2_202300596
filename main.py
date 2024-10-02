from flask import Flask, render_template, request
import os
import xml.etree.ElementTree as ET
from clases import Pila

app = Flask(__name__)

pila_maquinas = Pila()
pila_productos = Pila()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/archivo')
def archivo():
    return render_template('archivo.html')

@app.route('/cargar_archivo', methods=['GET', 'POST'])
def cargar_archivo():
    if 'fileInput' not in request.files:
        return "No se encontró el archivo"

    file = request.files['fileInput']
    if file.filename == '':
        return "No se seleccionó ningún archivo"
    
    if file:
        global pila_maquinas
        global pila_productos
        
        tree = ET.parse(file)
        root = tree.getroot()

        for child in root.findall('Maquina'):
            nombreMaquina = child.find('NombreMaquina').text
            produccion = int(child.find('CantidadLineasProduccion').text)
            componentes = int(child.find('CantidadComponentes').text)
            tiempo = int(child.find('TiempoEnsamblaje').text)
            
            # Insertamos la máquina
            pila_maquinas.insertMachine(nombreMaquina, produccion, componentes, tiempo)

            # Ahora buscamos los productos dentro de la máquina
            productos = child.find('ListadoProductos')
            if productos is not None:
                for producto in productos.findall('Producto'):
                    nombreProducto = producto.find('nombre').text
                    elaboracion = producto.find('elaboracion').text

                    # Insertamos el producto en la lista de productos
                    pila_productos.insertProduct(nombreProducto, elaboracion)

        # Imprimir para depurar
        print("Maquinas:")
        pila_maquinas.printMachine()
        print("\nProductos:")
        pila_productos.printProduct()

        return "Archivo cargado con éxito"

    
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')


if __name__ == '__main__':
    app.run(debug=True)
