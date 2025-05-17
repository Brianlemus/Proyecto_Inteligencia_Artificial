from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__, template_folder='../templates')

def read_tickets():
    tickets = []
    with open('ticket.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tickets.append(row)
    return tickets

def write_tickets(tickets):
    with open('ticket.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tickets)

@app.route('/')
def index():
    ticket = read_tickets()
    return render_template('editar_ticket.html', ticket=ticket)

@app.route('/edit/<int:ticket_id>', methods=['POST'])
def edit_ticket(ticket_id):
    tickets = read_tickets()
    
    # Actualizar datos del ticket
    tickets[ticket_id][1] = request.form['fecha']
    tickets[ticket_id][2] = request.form['prioridad']
    tickets[ticket_id][3] = request.form['area']
    tickets[ticket_id][4] = request.form['problema']
    tickets[ticket_id][5] = request.form['estado']
    
    # Guardar los cambios en el archivo CSV
    write_tickets(tickets)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)