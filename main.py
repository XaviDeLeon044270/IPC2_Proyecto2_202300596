from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/archivo')
def archivo():
    return render_template('archivo.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
    print('Servidor corriendo en http://localhost:5000/')