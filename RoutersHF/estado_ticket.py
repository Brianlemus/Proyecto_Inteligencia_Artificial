from flask import Flask, render_template, request, redirect, url_for
import csv
from pathlib import Path

app = Flask(__name__, template_folder='../templates')
CSV_FILE = Path('ticket.csv')

def read_tickets():
    """Lee los tickets desde el archivo CSV"""
    if not CSV_FILE.exists():
        return []
    
    with CSV_FILE.open(newline='', encoding='utf-8') as csvfile:
        return list(csv.reader(csvfile))

@app.route('/')
def index():
    """Muestra la lista de tickets"""
    ticket = read_tickets()
    return render_template('editar_ticket.html', ticket=ticket)

@app.route('/edit/<int:ticket_id>', methods=['POST'])
def edit_ticket(ticket_id):
    """Edita un ticket específico"""
    ticket = read_tickets()
    
    # Validar que el ticket_id existe
    if ticket_id < 0 or ticket_id >= len(ticket):
        return redirect(url_for('index'))
    
    # Actualizar datos del ticket
    updated_ticket = [
        request.form.get('ticket_number', ticket[ticket_id][0]),  # Mantener el número original
        request.form['fecha'],
        request.form['prioridad'],
        request.form['area'],
        request.form['problema'],
        request.form['estado']
    ]
    
    ticket[ticket_id] = updated_ticket
    
    # Guardar los cambios
    with CSV_FILE.open('w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerows(ticket)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)