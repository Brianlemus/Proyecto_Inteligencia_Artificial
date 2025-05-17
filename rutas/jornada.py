from flask import Flask, render_template, request, redirect, url_for, Blueprint
import csv
import os

jornada_bp = Blueprint('jornada', __name__, template_folder='templates',url_prefix='/jornada')

CSV_FILE = 'jornada.csv'

@jornada_bp.route('/ingreso_jornada', methods=['POST'])
def ingreso_jornada():
    dias = request.form['dias']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']

    # Escribir en el archivo CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dias, hora_inicio, hora_fin])
    
    return redirect(url_for('listado_jornada'))  # Redirige al listado

@jornada_bp.route('/listado_jornada')
def listado_jornada():
    # Leer los datos del CSV
    jornadas = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            jornadas = list(reader)  # Convertir a lista
    except FileNotFoundError:
        pass  # Maneja el caso en que el archivo no existe

    return render_template('listado_jornada.html', jornadas=jornadas)

@jornada_bp.route('/')
def index():
    return render_template('crear_jornada.html')