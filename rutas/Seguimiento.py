from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Ruta del archivo CSV donde se almacenan los tickets
TICKET_FILE = 'data/tickets.csv'

# Asegurar que la carpeta y archivo existen
os.makedirs('data', exist_ok=True)
if not os.path.exists(TICKET_FILE):
    with open(TICKET_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Categoría', 'Descripción', 'Fecha y Hora', 'Estado'])

# Ruta 1: Crear ticket
@app.route('/crear_ticket', methods=['GET', 'POST'])
def crear_ticket():
    if request.method == 'POST':
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Guardar en archivo CSV
        with open(TICKET_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([categoria, descripcion, fecha_hora, 'Pendiente'])

        return redirect(url_for('instrucciones', categoria=categoria))

    return render_template('crear_ticket.html')

# Ruta 2: Mostrar instrucciones según categoría
@app.route('/instrucciones/<categoria>')
def instrucciones(categoria):
    soluciones = {
        'agua': [
            "Cerrar la válvula principal.",
            "Colocar un tapón temporal.",
            "Contactar a mantenimiento si continúa el problema."
        ],
        'electricidad': [
            "Verificar interruptores y focos.",
            "Revisar si hay apagón en la zona.",
            "Contactar al encargado si el problema persiste."
        ],
        'seguridad': [
            "Comunicar al personal de seguridad.",
            "Evitar enfrentamientos directos.",
            "Llamar al número de emergencia del residencial."
        ]
    }

    pasos = soluciones.get(categoria.lower(), ["No hay instrucciones disponibles para esta categoría."])
    return render_template('instrucciones.html', categoria=categoria.capitalize(), pasos=pasos)

# Ruta 3: Listado de tickets
@app.route('/listado_tickets')
def listado_tickets():
    tickets = []
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            tickets = list(reader)[1:]  # Saltar encabezado
    return render_template('listado_tickets.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
