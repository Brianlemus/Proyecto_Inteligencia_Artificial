from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    # Leer opciones del archivo area.csv
    areas = []
    with open('area.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            areas.append(row)  

    return render_template('crear_puesto.html', areas=areas)

@app.route('/crear_puesto', methods=['POST'])
def crear_puesto():
    area_id = request.form['area']
    puesto_nombre = request.form['puesto']

    # Guardar en puesto.csv
    with open('puesto.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([area_id, puesto_nombre])  # Guardar el área y el nombre del puesto

    return redirect(url_for('lista_puesto'))

@app.route('/lista_puesto')
def lista_puesto():
    # Leer los datos del CSV
    puestos = []
    try:
        with open('puesto.csv', mode='r') as file:
            reader = csv.reader(file)
            puestos = list(reader)  # Convertir a lista
    except FileNotFoundError:
        pass  # Maneja el caso en que el archivo no existe

    return render_template('lista_puesto.html', puestos=puestos)

if __name__ == '__main__':
    app.run(debug=True)