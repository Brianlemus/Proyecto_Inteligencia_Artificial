from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para mensajes flash

# Ruta para la página principal que muestra los tickets
@app.route('/')
def index():
    tickets = []
    if os.path.exists('ticket.csv'):
        with open('ticket.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            tickets = [row for row in reader]
    return render_template('tabla_ticket.html', tickets=tickets)

# Ruta para la página de seguimiento de tickets
@app.route('/seguimiento_ticket', methods=['GET', 'POST'])
def seguimiento_ticket():
    # Aquí puedes agregar lógica para manejar la actualización o eliminación de tickets
    tickets = []
    if os.path.exists('ticket.csv'):
        with open('ticket.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            tickets = [row for row in reader]
    return render_template('seguimiento.html', tickets=tickets)

if __name__ == '__main__':
    if not os.path.exists('ticket.csv'):
        with open('ticket.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Número", "Fecha", "Prioridad", "Área", "Problema", "Estado"])
    
    app.run(debug=True)