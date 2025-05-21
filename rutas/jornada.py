from flask import Blueprint, render_template, request, flash
import os
import csv
from utils import csv_utils

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
JORNADA_CSV = os.path.join(DATA_DIR, 'jornada.csv')

jornada_bp = Blueprint('jornada', __name__, template_folder='templates', url_prefix='/jornada')

@jornada_bp.route('/')
def index():
    return render_template('crear_jornada.html')

@jornada_bp.route('/crear_jornada', methods=['POST'])
def crear_jornada():
    jornada_nombre = request.form['jornada'].strip()

    if not jornada_nombre:
        flash('El nombre de la jornada no puede estar vacío.', 'danger')
        return render_template('crear_jornada.html')

    jornadas = csv_utils.read_csv(JORNADA_CSV)

    # Obtener nuevo ID autoincremental
    if jornadas:
        try:
            last_id = max(int(j[0]) for j in jornadas if j[0].isdigit())
        except ValueError:
            last_id = 0
        new_id = last_id + 1
    else:
        new_id = 1

    try:
        with open(JORNADA_CSV, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([new_id, jornada_nombre])
        flash('Jornada creada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al guardar la jornada: {e}', 'danger')

    return render_template('crear_jornada.html')

@jornada_bp.route('/lista_jornada')
def lista_jornada():
    jornadas = csv_utils.read_csv(JORNADA_CSV)
    return render_template('lista_jornada.html', jornadas=jornadas)
