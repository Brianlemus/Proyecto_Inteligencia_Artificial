from flask import Flask, render_template, request, redirect, url_for,Blueprint,flash
import os
import csv
from utils import csv_utils



DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

PUESTO_CSV = os.path.join(DATA_DIR, 'puesto.csv')


puesto_bp = Blueprint('puesto', __name__, template_folder='templates',url_prefix='/puesto')

@puesto_bp.route('/')
def index():    
    return render_template('crear_puesto.html')

@puesto_bp.route('/crear_puesto', methods=['POST'])
def crear_puesto():
    puesto_nombre = request.form['puesto'].strip()

    if not puesto_nombre:
        flash('El nombre del puesto no puede estar vacío.', 'danger')
        return render_template('crear_puesto.html')

    # Leer los puestos existentes
    puestos = csv_utils.read_csv(PUESTO_CSV)

    # Obtener nuevo ID autoincremental
    if puestos:
        last_id = max(int(p[0]) for p in puestos)
        new_id = last_id + 1
    else:
        new_id = 1

    try:
        # Guardar nuevo puesto
        with open(PUESTO_CSV, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([new_id, puesto_nombre])
        flash('Puesto creado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al guardar el puesto: {e}', 'danger')

    return render_template('crear_puesto.html')




@puesto_bp.route('/lista_puesto')
def lista_puesto():
    puestos = csv_utils.read_csv(os.path.join(DATA_DIR, 'puesto.csv'))
    return render_template('lista_puesto.html', puestos=puestos)