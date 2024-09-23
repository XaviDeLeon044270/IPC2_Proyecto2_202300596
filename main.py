from flask import Flask, render_template

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/archivo', 'archivo', self.archivo)
        self.app.add_url_rule('/info', 'info', self.info)
        self.app.add_url_rule('/reportes', 'reportes', self.reportes)

    def home(self):
        return render_template('index.html')

    def archivo(self):
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