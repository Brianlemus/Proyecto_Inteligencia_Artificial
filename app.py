from flask import Flask, render_template, request,jsonify,session, redirect, url_for
import csv
import os
from rutas.jornada import jornada_bp  # importar el blueprint
from rutas.puesto import puesto_bp  # importar el blueprint
from rutas.area import area_bp 
from utils.csv_utils import leer_direcciones,leer_tipos_puesto,leer_jornadas,leer_areas,guardar_csv,leer_trabajadores, leer_residentes, leer_usuarios,read_csv

app = Flask(__name__)
app.secret_key = '12345'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@app.route('/')
def index():    
    return render_template('login.html')


@app.route('/crear')
def crear():
    direcciones = leer_direcciones()
    tipos = leer_tipos_puesto()
    jornadas=leer_jornadas()
    areas=leer_areas()
    return render_template('crear_usuario.html',direcciones=direcciones,tipos_puesto=tipos,jornadas=jornadas,areas=areas)


@app.route('/guardar_residente', methods=['POST'])
def guardar_residente():
    error = None
    mensaje = None
    data = request.form

    campos = ['dpi', 'nit', 'nombre_completo', 'apellidos', 'telefono',
              'fecha_nacimiento', 'correo_electronico', 'direccion_id']

    fila = {
        'dpi': data.get('dpi', '').strip(),
        'nit': data.get('nit', '').strip(),
        'nombre_completo': data.get('nombre_completo', '').strip(),
        'apellidos': data.get('apellidos', '').strip(),
        'telefono': data.get('telefono', '').strip(),
        'fecha_nacimiento': data.get('fecha_nacimiento', '').strip(),
        'correo_electronico': data.get('correo', '').strip(),
        'direccion_id': data.get('direccion_id', '').strip()
    }

    for campo in campos:
        if not fila[campo]:
            error = f'Falta el campo {campo}'
            break

    if not error:
        ruta_residentes = os.path.join(DATA_DIR, 'residentes.csv')
        ruta_trabajadores = os.path.join(DATA_DIR, 'trabajadores.csv')

        residentes = read_csv(ruta_residentes)
        trabajadores = read_csv(ruta_trabajadores)

        correos = [r[6].lower() for r in residentes[1:] + trabajadores[1:] if len(r) > 6]
        dpis = [r[0] for r in residentes[1:] + trabajadores[1:] if len(r) > 0]

        if fila['correo_electronico'].lower() in correos:
            error = 'El correo ya está registrado en el sistema.'
        elif fila['dpi'] in dpis:
            error = 'El DPI ya está registrado en el sistema.'

    if not error:
        guardar_csv(ruta_residentes, campos, fila)
        mensaje = "Residente guardado correctamente."

    return render_template(
        'crear_usuario.html',
        mensaje=mensaje,
        error=error,
        direcciones=leer_direcciones(),
        tipos_puesto=leer_tipos_puesto(),
        jornadas=leer_jornadas(),
        areas=leer_areas()
    )


@app.route('/guardar_trabajador', methods=['POST'])
def guardar_trabajador():
    error = None
    mensaje = None
    data = request.form

    campos = ['dpi', 'nit', 'nombre_completo', 'apellidos', 'telefono',
              'fecha_nacimiento', 'correo_electronico',
              'salario', 'tipo_puesto', 'jornada', 'area']

    fila = {
        'dpi': data.get('dpi', '').strip(),
        'nit': data.get('nit', '').strip(),
        'nombre_completo': data.get('nombre_completo', '').strip(),
        'apellidos': data.get('apellidos', '').strip(),
        'telefono': data.get('telefono', '').strip(),
        'fecha_nacimiento': data.get('fecha_nacimiento', '').strip(),
        'correo_electronico': data.get('correo', '').strip(),        
        'salario': data.get('salario', '').strip(),
        'tipo_puesto': data.get('tipo_puesto', '').strip(),
        'jornada': data.get('tipo_jornada', '').strip(),
        'area': data.get('area_id', '').strip()
    }

    for campo in campos:
        if not fila[campo]:
            error = f'Falta el campo {campo}'
            break

    if not error:
        ruta_trabajadores = os.path.join(DATA_DIR, 'trabajadores.csv')
        ruta_residentes = os.path.join(DATA_DIR, 'residentes.csv')

        trabajadores = read_csv(ruta_trabajadores)
        residentes = read_csv(ruta_residentes)

        correos = [r[6].lower() for r in residentes[1:] + trabajadores[1:] if len(r) > 6]
        dpis = [r[0] for r in residentes[1:] + trabajadores[1:] if len(r) > 0]

        if fila['correo_electronico'].lower() in correos:
            error = 'El correo ya está registrado en el sistema.'
        elif fila['dpi'] in dpis:
            error = 'El DPI ya está registrado en el sistema.'

    if not error:
        guardar_csv(ruta_trabajadores, campos, fila)
        mensaje = "Trabajador guardado correctamente."

    return render_template(
        'crear_usuario.html',
        mensaje=mensaje,
        error=error,
        direcciones=leer_direcciones(),
        tipos_puesto=leer_tipos_puesto(),
        jornadas=leer_jornadas(),
        areas=leer_areas()
    )




@app.route('/listado')
def ver_datos():
    trabajadores = leer_trabajadores()
    residentes = leer_residentes()
    usuarios = leer_usuarios()
    return render_template('listado.html',
                           trabajadores=trabajadores,
                           residentes=residentes,
                           usuarios=usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        ruta_csv = os.path.join(DATA_DIR, 'usuarios.csv')

        # Usuario admin por defecto
        admin_default = {
            'dpi': '0000000000000',
            'correo_electronico': 'admin@admin.com',
            'username': 'admin',
            'password': 'admin123',
            'rol': 'administrador'
        }

        # Validar usuario admin por defecto
        if username == admin_default['username'] and password == admin_default['password']:
            session['username'] = admin_default['username']
            session['rol'] = admin_default['rol']
            return redirect(url_for('menu_admin'))

        # Buscar usuario en CSV por username
        if os.path.exists(ruta_csv):
            with open(ruta_csv, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'].strip() == username and row['password'].strip() == password:
                        session['username'] = row['username'].strip()
                        session['rol'] = row['rol'].strip().lower()
                        return redirect(url_for('menu_admin'))

        return render_template('login.html', error="Credenciales incorrectas.")

    return render_template('login.html')


@app.route('/menuAdmin')
def menu_admin():
    if 'username' not in session:
        return redirect(url_for('login'))

    rol = session.get('rol', '')
    username = session.get('username', '')

    # Renderiza la vista con los datos de sesión para controlar acceso/visibilidad
    return render_template('menuAdmin.html', rol=rol, username=username)

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    dpi = request.form['dpi'].strip()
    correo = request.form['correo'].strip()
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    rol = request.form['rol'].strip().lower()

    ruta_usuarios = os.path.join(DATA_DIR, 'usuarios.csv')
    rutas_roles = {
        'residente': os.path.join(DATA_DIR, 'residentes.csv'),
        'trabajador': os.path.join(DATA_DIR, 'trabajadores.csv')
    }

    if rol not in rutas_roles:
        return render_template('registro.html', error="Rol inválido. Selecciona residente o trabajador.")

    # Verificar si ya existe ese username, dpi o correo en usuarios (independientemente del rol)
    if os.path.exists(ruta_usuarios):
        with open(ruta_usuarios, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila['username'].strip() == username:
                    return render_template('registro.html', error="Nombre de usuario ya registrado.")
                if fila['dpi'].strip() == dpi and fila['rol'].strip().lower() == rol:
                    return render_template('registro.html', error=f"Ese DPI ya tiene una cuenta de {rol}.")
                if fila['correo_electronico'].strip().lower() == correo.lower() and fila['rol'].strip().lower() == rol:
                    return render_template('registro.html', error=f"Ese correo ya está registrado como {rol}.")

    # Verificar si el DPI y correo existen en el archivo de su rol (residente o trabajador)
    ruta_fuente = rutas_roles[rol]
    if not os.path.exists(ruta_fuente):
        return render_template('registro.html', error=f"No se encontró el archivo de {rol}s.")

    existe_en_rol = False
    with open(ruta_fuente, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['dpi'].strip() == dpi and fila.get('correo_electronico', '').strip().lower() == correo.lower():
                existe_en_rol = True
                break

    if not existe_en_rol:
        return render_template('registro.html', error=f"El DPI y el correo no existen en el archivo de {rol}s.")

    # Guardar nuevo usuario
    nuevo_usuario = {
        'dpi': dpi,
        'correo_electronico': correo,
        'username': username,
        'password': password,
        'rol': rol
    }

    archivo_nuevo = not os.path.exists(ruta_usuarios)
    with open(ruta_usuarios, 'a', newline='', encoding='utf-8') as archivo:
        fieldnames = ['dpi', 'correo_electronico', 'username', 'password', 'rol']
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        if archivo_nuevo:
            escritor.writeheader()
        escritor.writerow(nuevo_usuario)

    return render_template('registro.html', mensaje="Usuario registrado exitosamente.")


@app.route('/registro')
def registro_usuario():
    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.clear()  # Limpia toda la sesión
    return redirect(url_for('login'))  # Redirige a la página de login

app.register_blueprint(jornada_bp)  # registrar las rutas
app.register_blueprint(puesto_bp)  # registrar las rutas
app.register_blueprint(area_bp)  # registrar las rutas

if __name__ == '__main__':
    app.run(debug=True)