from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# Ruta de inicio que muestra el formulario login
@app.route('/')
def index():
    return render_template('login.html')

# Ruta que procesa el formulario
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Leer CSV y validar usuario
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email and row['password'] == password:
                return render_template('menuAdmin.html')
    
    # Si llega aquí, credenciales inválidas
    return render_template('login.html', error="Credenciales incorrectas")

if __name__ == '__main__':
    app.run(debug=True)

