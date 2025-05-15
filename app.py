from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if os.path.exists('users.csv'):
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email and row['password'] == password:
                    return render_template('menuAdmin.html')

    # Esta línea debe estar dentro de la función
    return render_template('login.html', error="Credenciales incorrectas")

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    roles, puestos, casas = [], [], []

    if os.path.exists('roles.csv'):
        with open('roles.csv', newline='') as f:
            reader = csv.DictReader(f)
            roles = [row['rol'] for row in reader]

    if os.path.exists('puestos.csv'):
        with open('puestos.csv', newline='') as f:
            reader = csv.DictReader(f)
            puestos = [row['puesto'] for row in reader]

    if os.path.exists('casas.csv'):
        with open('casas.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and all(row.values()):
                    casas.append(row)

    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']
        nombre = request.form['nombre']
        rol = request.form['rol']
        puesto = request.form['puesto']
        direccion = request.form['direccion']
        numero = request.form['numero']
        letra = request.form['letra']
        telefono = request.form['telefono']
        nombre_casa = request.form['nombre_casa']
        casa_id_form = request.form.get('selectorCasa')

        if os.path.exists('users.csv'):
            with open('users.csv', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['email'] == correo:
                        return render_template('registro.html',
                            error="Este correo ya está registrado.",
                            roles=roles, puestos=puestos, casas=casas)

        with open('users.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['email', 'password', 'nombre', 'rol', 'puesto'])
            writer.writerow([correo, clave, nombre, rol, puesto])

        #Crea casa si no se seleccionó una existente
        if casa_id_form:
            casa_id = casa_id_form
        else:
            casa_id = sum(1 for _ in open('casas.csv')) if os.path.exists('casas.csv') else 1
            with open('casas.csv', 'a', newline='\n') as f:
                writer = csv.writer(f)
                if f.tell() == 0:
                    writer.writerow(['id', 'direccion', 'numero', 'letra', 'telefono', 'nombre_casa'])
                writer.writerow([casa_id, direccion, numero, letra, telefono, nombre_casa])

        with open('usuarios_casas.csv', 'a', newline='\n') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['email', 'casa_id'])
            writer.writerow([correo, casa_id])

        return f'Usuario {correo} registrado exitosamente.'

    return render_template('registro.html', roles=roles, puestos=puestos, casas=casas)

if __name__ == '__main__':
    app.run(debug=True)