from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv
import os
from pathlib import Path

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para mensajes flash
CSV_FILE = Path('ticket.csv')
DICCIONARIO_FILE = Path('diccionario.csv')

def cargar_diccionario():
    diccionario = {}
    try:
        with DICCIONARIO_FILE.open(mode='r', encoding='utf-8', errors='replace') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                area = fila['Area']
                problema = fila['Problema']
                solucion = fila['Solucion']
                prioridad = fila['Prioridad']
                if problema not in diccionario:
                    diccionario[problema] = {'soluciones': [], 'area': area, 'prioridad': prioridad}
                diccionario[problema]['soluciones'].append(solucion)
    except FileNotFoundError:
        flash("El archivo diccionario.csv no existe", "error")
    return diccionario

diccionario = cargar_diccionario()

def obtener_numero_ticket():
    if not CSV_FILE.exists():
        return 1
    with CSV_FILE.open(mode='r', encoding='utf-8', errors='replace') as file:
        reader = csv.reader(file)
        tickets = list(reader)
        return len(tickets) + 1

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        data = diccionario.get(descripcion, None)
        
        if data:
            area = data['area']
            soluciones = data['soluciones']
            prioridad = data['prioridad']
        else:
            area = "Área desconocida"
            soluciones = ["No se encontró solución para el problema."]
            prioridad = "Por definirse"

        resultado = f"<h5>Área</h5><li>{area}</li><h5>Descripción</h5><li>{descripcion}</li><h5>Solución</h5><ul>"
        for solucion in soluciones:
            resultado += f"<li>{solucion}</li>"
        resultado += "</ul>"

        numero_ticket = obtener_numero_ticket()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = "Espera"

        with CSV_FILE.open(mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([numero_ticket, fecha, prioridad, area, descripcion, estado])  

        return redirect(url_for('mostrar_respuesta', resultado=resultado))

    return render_template('crearticket.html')

@app.route('/mostrar_respuesta')
def mostrar_respuesta():
    resultado = request.args.get('resultado', '')
    return render_template('solucion.html', resultado=resultado)

@app.route('/seguimiento_ticket', methods=['GET', 'POST'])
def seguimiento_ticket():
    if request.method == 'POST':
        leido = request.form.get('leido')
        resuelto = request.form.get('resuelto')

        tickets = []
        if CSV_FILE.exists():
            with CSV_FILE.open(mode='r', encoding='utf-8', errors='replace') as file:
                reader = csv.reader(file)
                tickets = list(reader)

        if leido == "si" and resuelto == "si":
            if tickets and tickets[-1][5] == "Espera":
                tickets.pop()
                with CSV_FILE.open(mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(tickets)
                flash("No se generó ticket ya que el problema fue resuelto", "success")
                return redirect(url_for('barra'))
            else:
                flash("No hay tickets pendientes para cancelar", "info")
                return redirect(url_for('barra'))

        elif resuelto in ["no", "no_completamente"]:
            flash("Ticket generado correctamente", "success")
            return redirect(url_for('seguimiento_ticket'))

    tickets = []
    try:
        with CSV_FILE.open(mode='r', encoding='utf-8', errors='replace') as file:
            reader = csv.reader(file)
            tickets = list(reader)
    except FileNotFoundError:
        flash("No hay tickets generados aún", "info")

    return render_template('seguimiento.html', ticket=tickets)


@app.route('/editar_ticket', methods=['GET'])
def index():
    ticket = read_tickets()
    return render_template('editar_ticket.html', ticket=ticket)

def read_tickets():
    if not CSV_FILE.exists():
        return []
    
    with CSV_FILE.open(newline='', encoding='utf-8', errors='replace') as csvfile:
        return list(csv.reader(csvfile))

@app.route('/edit/<int:ticket_id>', methods=['POST'])
def edit_ticket(ticket_id):
    ticket = read_tickets()
    
    if ticket_id < 0 or ticket_id >= len(ticket):
        return redirect(url_for('index'))
    
    updated_ticket = [
        request.form.get('ticket_number', ticket[ticket_id][0]),
        request.form['fecha'],
        request.form['prioridad'],
        request.form['area'],
        request.form['problema'],
        request.form['estado']
    ]
    
    ticket[ticket_id] = updated_ticket
    
    with CSV_FILE.open('w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerows(ticket)
    
    return redirect(url_for('index'))

@app.route('/barra')
def barra():
    return render_template('menuAdmin.html')

if __name__ == '__main__':
    if not CSV_FILE.exists():
        with CSV_FILE.open(mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Número", "Fecha", "Prioridad", "Área", "Problema", "Estado"])
    
    if not DICCIONARIO_FILE.exists():
        with DICCIONARIO_FILE.open(mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Area", "Problema", "Solucion", "Prioridad"])
    
    app.run(debug=True)