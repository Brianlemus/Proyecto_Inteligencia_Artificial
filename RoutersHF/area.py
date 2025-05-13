from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv


app = Flask(__name__, template_folder='../templates')
app.secret_key = 'secret_key'


CSV_FILE = os.path.join(os.path.dirname(__file__), '..', 'area.csv')


def obtener_siguiente_id():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return 1  
    with open(CSV_FILE, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        filas = list(lector)
        if filas:  
            return int(filas[-1][0]) + 1
        else:  
            return 1


def verificar_encabezados():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['id', 'area'])  


@app.route('/')
def formulario():
    return render_template('crear_area.html')


@app.route('/guardar_area', methods=['POST'])
def guardar_area():
    nombre_area = request.form.get('nombre_area')

    if nombre_area:
        with open(CSV_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            areas = [row[1] for row in lector]  
        
        if nombre_area in areas:
            flash('El área ya existe.', 'danger') 
            return redirect(url_for('formulario'))
        
        nuevo_id = obtener_siguiente_id()

        
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([nuevo_id, nombre_area])

        flash('Área creada con éxito.', 'success')
        return redirect(url_for('listado'))
    else:
        flash('Debe ingresar un nombre de área.', 'danger')
        return redirect(url_for('formulario'))


@app.route('/listado')
def listado():
    areas = []
    verificar_encabezados()

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            areas = list(lector)

    return render_template('lista_area.html', areas=areas)

if __name__ == '__main__':
    app.run(debug=True)