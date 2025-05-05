from flask import Flask, render_template
import os
import csv

app = Flask(__name__, template_folder='../templates')

CSV_FILE = os.path.join(os.path.dirname(__file__), '..', 'area.csv')

@app.route('/')
def index():
    return render_template('lista_area.html')

@app.route('/listado')
def listado():
    areas = []

    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector, None)  # Saltar la primera fila (encabezado)
                areas = list(lector)
        except Exception as e:
            return f"Error al leer el archivo CSV: {e}"
    else:
        return f"Archivo no encontrado en la ruta: {CSV_FILE}"

    return render_template('lista_area.html', areas=areas)

if __name__ == '__main__':
    app.run(debug=True)
