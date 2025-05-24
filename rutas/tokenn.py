from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import csv
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para mensajes flash

def cargar_diccionario():
    diccionario = {}
    try:
        with open('diccionario.csv', mode='r', encoding='utf-8') as archivo:
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
    except UnicodeDecodeError as e:
        flash(f"Error de codificación: {str(e)}", "error")
    return diccionario

diccionario = cargar_diccionario()

def obtener_numero_ticket():
    if not os.path.exists('ticket.csv'):
        return 1
    with open('ticket.csv', mode='r', encoding='utf-8') as file:
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

        # Generar ticket provisional
        numero_ticket = obtener_numero_ticket()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = "Espera"

        with open('ticket.csv', mode='a', newline='', encoding='utf-8') as csvfile:
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

        # Leer todos los tickets
        tickets = []
        if os.path.exists('ticket.csv'):
            with open('ticket.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                tickets = list(reader)

        # Si ambas respuestas son "Sí", eliminar el último ticket en espera
        if leido == "si" and resuelto == "si":
            if tickets and tickets[-1][5] == "Espera":  # Verificar que el último está en espera
                tickets.pop()
                with open('ticket.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(tickets)
                flash("No se generó ticket ya que el problema fue resuelto", "success")
                return redirect(url_for('barra'))
            else:
                flash("No hay tickets pendientes para cancelar", "info")
                return redirect(url_for('barra'))

        # Si no se resolvió, mantener el ticket generado previamente
        elif resuelto in ["no", "no_completamente"]:
            flash("Ticket generado correctamente", "success")
            return redirect(url_for('seguimiento_ticket'))

    # Mostrar tickets existentes
    tickets = []
    try:
        with open('ticket.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            tickets = list(reader)
    except FileNotFoundError:
        flash("No hay tickets generados aún", "info")

    return render_template('seguimiento.html', ticket=tickets)

@app.route('/barra')
def barra():
    return render_template('menuAdmin.html')

if __name__ == '__main__':
    if not os.path.exists('ticket.csv'):
        with open('ticket.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Número", "Fecha", "Prioridad", "Área", "Problema", "Estado"])
    
    if not os.path.exists('diccionario.csv'):
        with open('diccionario.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Area", "Problema", "Solucion", "Prioridad"])
    
    app.run(debug=True)