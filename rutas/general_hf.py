from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
import pandas as pd # Instalación nueva
import matplotlib.pyplot as plt # Instalación nueva
from io import BytesIO # Instalación nueva
import base64 # Instalación nueva
import csv
import os
from pathlib import Path

ticket_bp = Blueprint('ticket', __name__, template_folder='templates', url_prefix='/ticket')

#ticket_bp.secret_key = 'tu_clave_secreta_aqui'  # Necesario para mensajes flash
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

def generar_grafica_pie_area():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(conteo_areas, labels=conteo_areas.index, autopct='%1.1f%%', startangle=140)
    plt.title('Porcentajes en Areas')
    plt.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_pie_prioridad():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_prioridad = df['prioridad'].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(conteo_prioridad, labels=conteo_prioridad.index, autopct='%1.1f%%', startangle=140)
    plt.title('Porcentaje de Prioridad')
    plt.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_barras_area():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightpink']
    conteo_areas.plot(kind='bar', color=colores[:len(conteo_areas)])
    plt.title('Total de tickets por Area')
    plt.xlabel('Area')
    plt.ylabel('Numero de Tickets')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_barras_prioridad():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_prioridad = df['prioridad'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightpink']
    conteo_prioridad.plot(kind='bar', color=colores[:len(conteo_prioridad)])
    plt.title('Total de tickets por prioridad')
    plt.xlabel('Prioridad')
    plt.ylabel('Número de Tickets')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

@ticket_bp.route('/barra')
def barra():
    return render_template('menuAdmin.html')

@ticket_bp.route('/crear_ticket', methods=['GET', 'POST'])
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

@ticket_bp.route('/mostrar_respuesta')
def mostrar_respuesta():
    resultado = request.args.get('resultado', '')
    return render_template('solucion.html', resultado=resultado)

@ticket_bp.route('/seguimiento_ticket', methods=['GET', 'POST'])
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
                return redirect(url_for('index'))
            else:
                flash("No hay tickets pendientes para cancelar", "info")
                return redirect(url_for('index'))

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

@ticket_bp.route('/editar_ticket', methods=['GET'])
def editar_ticket():
    ticket = read_tickets()
    return render_template('editar_ticket.html', ticket=ticket)

def read_tickets():
    if not CSV_FILE.exists():
        return []
    
    with CSV_FILE.open(newline='', encoding='utf-8', errors='replace') as csvfile:
        return list(csv.reader(csvfile))

@ticket_bp.route('/edit/<int:ticket_id>', methods=['POST'])
def edit_ticket(ticket_id):
    ticket = read_tickets()
    
    if ticket_id < 0 or ticket_id >= len(ticket):
        return redirect(url_for('editar_ticket'))
    
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
    
    return redirect(url_for('editar_ticket'))

@ticket_bp.route('/grafica_pie_area')
def mostrar_grafica_pie_area():
    imagen = generar_grafica_pie_area()
    if imagen:
        return render_template('pie_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@ticket_bp.route('/grafica_pie_prioridad')
def mostrar_grafica_pie_prioridad():
    imagen = generar_grafica_pie_prioridad()
    if imagen:
        return render_template('pie_prioridad.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@ticket_bp.route('/grafica_barras_area')
def mostrar_grafica_barras_area():
    imagen = generar_grafica_barras_area()
    if imagen:
        return render_template('barras_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@ticket_bp.route('/grafica_barras_prioridad')
def mostrar_grafica_barras_prioridad():
    imagen = generar_grafica_barras_prioridad()
    if imagen:
        return render_template('barras_prioridad.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

