from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os

app = Flask(__name__, template_folder='../templates')

def cargar_diccionario():
    diccionario = {}
    with open('diccionario.csv', mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            area = fila['Area']
            problema = fila['Problema']
            solucion = fila['Solucion']
            if problema not in diccionario:
                diccionario[problema] = {'soluciones': [], 'area': area}
            diccionario[problema]['soluciones'].append(solucion)
    return diccionario

diccionario = cargar_diccionario()

def obtener_numero_ticket():
    if not os.path.exists('ticket.csv'):
        return 1
    with open('ticket.csv', mode='r') as file:
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
        else:
            area = "Área desconocida"
            soluciones = ["No se encontró solución para el problema."]
        
        resultado = f"<h5>Área</h5><li>{area}</li><h5>Descripción</h5><li>{descripcion}</li><h5>Solución</h5><ul>"
        for solucion in soluciones:
            resultado += f"<li>{solucion}</li>"
        resultado += "</ul>"

        # Generar ticket aunque la descripción sea desconocida
        numero_ticket = obtener_numero_ticket()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = "espera"

        with open('ticket.csv', mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([numero_ticket, fecha, area, descripcion, estado])

        return redirect(url_for('mostrar_respuesta', resultado=resultado))

    return render_template('crearticket.html')

@app.route('/mostrar_respuesta')
def mostrar_respuesta():
    resultado = request.args.get('resultado', '')
    return render_template('solucion.html', resultado=resultado)

@app.route('/seguimiento_ticket', methods=['GET', 'POST'])
def seguimiento_ticket():
    ticket = []
    if request.method == 'POST':
        leido = request.form.get('leido')
        resuelto = request.form.get('resuelto')

        if leido == "si" and resuelto == "si":
            return redirect(url_for('barra'))  # No generar ticket

        # Generar ticket si la respuesta es "No" o "No completamente"
        if resuelto in ["no", "no_completamente"]:
            numero_ticket = obtener_numero_ticket()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado = "espera"

            with open('ticket.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([numero_ticket, fecha, "Área desconocida", "Descripción del problema", estado])
            return redirect(url_for('seguimiento_ticket'))

    try:
        with open('ticket.csv', mode='r') as file:
            reader = csv.reader(file)
            ticket = list(reader) 
    except FileNotFoundError:
        pass

    return render_template('seguimiento.html', ticket=ticket)

@app.route('/barra')
def barra():
    return render_template('menuAdmin.html')

if __name__ == '__main__':
    app.run(debug=True)