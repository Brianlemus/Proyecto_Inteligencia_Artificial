from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__, template_folder='../templates')
CSV_FILE = 'jornada.csv'

@app.route('/ingreso_jornada', methods=['POST'])  # Corregido 'method' a 'methods'
def ingreso_jornada():
    dias = request.form['dias']  # Asegúrate de usar el nombre correcto
    hora_inicio = request.form['hora_inicio']  # Asegúrate de usar el nombre correcto
    hora_fin = request.form['hora_fin']  # Asegúrate de usar el nombre correcto

    # Escribir en el archivo CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dias, hora_inicio, hora_fin])
    
    return render_template('listado_jornada.html')

@app.route('/listado_jornada')
def listado_jornada():
    return render_template('listado_jornada.html')


@app.route('/')
def index():
    return render_template('crear_jornada.html')

if __name__ == '__main__':
    app.run(debug=True)