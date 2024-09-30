from flask import Flask, render_template, request
import os
from xml.etree import ElementTree
from werkzeug.utils import secure_filename

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/archivo', 'archivo', self.archivo, methods=['GET', 'POST'])
        self.app.add_url_rule('/info', 'info', self.info)
        self.app.add_url_rule('/reportes', 'reportes', self.reportes)

    def home(self):
        return render_template('index.html')

    def archivo(self):
        if request.method == 'POST':
            file = request.files.get('fileInput')
            if file and file.filename.endswith('.xml'):
                filename = secure_filename(file.filename)
                file.save(os.path.join('uploads', filename))
                return 'Archivo subido con éxito'
            else:
                return 'No se seleccionó ningún archivo o el archivo no es válido'
        else:
            return render_template('archivo.html')

    def info(self):
        return render_template('info.html')

    def reportes(self):
        return render_template('reportes.html')

    def run(self):
        self.app.run(host='localhost', debug=True)
        print('Servidor corriendo en http://localhost:5000/')

if __name__ == '__main__':
    app = MyApp()
    app.run()