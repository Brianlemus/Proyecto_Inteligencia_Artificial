from flask import Blueprint, render_template, request, flash
import os
import csv
from utils import csv_utils

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
AREA_CSV = os.path.join(DATA_DIR, 'area.csv')

area_bp = Blueprint('area', __name__, template_folder='templates', url_prefix='/area')


@area_bp.route('/')
def index():
    return render_template('crear_area.html')


@area_bp.route('/crear_area', methods=['POST'])
def crear_area():
    area_nombre = request.form['area'].strip()

    if not area_nombre:
        flash('El nombre del área no puede estar vacío.', 'danger')
        return render_template('crear_area.html')

    # Leer áreas existentes
    areas = csv_utils.read_csv(AREA_CSV)

    # Generar nuevo ID autoincremental
    try:
        if areas:
            last_id = max(int(a[0]) for a in areas if a[0].isdigit())
            new_id = last_id + 1
        else:
            new_id = 1
    except Exception as e:
        flash(f'Error al procesar el archivo CSV: {e}', 'danger')
        return render_template('crear_area.html')

    # Guardar nueva área
    try:
        with open(AREA_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([new_id, area_nombre])
        flash('Área creada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al guardar el área: {e}', 'danger')

    return render_template('crear_area.html')


@area_bp.route('/lista_area')
def lista_area():
    areas = csv_utils.read_csv(AREA_CSV)
    return render_template('lista_area.html', areas=areas)
