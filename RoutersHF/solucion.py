import csv
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DICCIONARIO_CSV = 'data/diccionario.csv'

@app.route('/instrucciones/<categoria>/<problema>', methods=['GET', 'POST'])
def instrucciones(categoria, problema):
    pasos = []

    # Leer pasos desde diccionario.csv
    if os.path.exists(DICCIONARIO_CSV):
        with open(DICCIONARIO_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Area'].lower() == categoria.lower() and row['Problema'].lower() == problema.lower():
                    pasos.append(row['Solucion'])

    mensaje = ""
    mostrar_ticket = False

    if request.method == 'POST':
        leido = request.form.get('leido')
        resuelto = request.form.get('resuelto')

        if leido == 'no':
            mensaje = "Por favor lea las instrucciones antes de continuar."
        elif leido == 'si':
            if resuelto == 'si':
                mensaje = "¡Perfecto! No es necesario generar un ticket."
            elif resuelto in ['no', 'no_completamente']:
                mensaje = "Ticket generado correctamente."
                mostrar_ticket = True

    return render_template('instrucciones.html',
                           categoria=categoria.capitalize(),
                           problema=problema.capitalize(),
                           pasos=pasos,
                           mensaje=mensaje,
                           mostrar_ticket=mostrar_ticket)
