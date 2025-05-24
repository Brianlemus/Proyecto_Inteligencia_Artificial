from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('menuAdmin.html')

@app.route('/home')
def home():
    return render_template('menuAdmin.html')

@app.route('/crear_tickets')
def crear_tickets():
    return render_template('crearticket.html')

@app.route('/historial_tickets')
def historial_ticket():
    return render_template('seguimiento.html')


@app.route('/grafica_pie')
def grafica_pie():
    return render_template('grafica_pie.html')


@app.route('/grafica_barra')
def grafica_barra():
    return render_template('grafica_barras.html')

@app.route('/crear_empleado')
def crear_empleado():
    return render_template('crear_usuario.html')

@app.route('/listado_empleado')
def listado_empleado():
    return  render_template('listado_empleado.html')

@app.route('/crear_puesto')
def crear_puesto():
    return render_template('crear_puesto.html')

@app.route('/listado_puesto')
def listado_puesto():
    return render_template('lista_puesto.html')

@app.route('/crear_area')
def crear_area():
    return render_template('crear_area.html')


@app.route('/listado_area')
def listado_area():
    return render_template('lista_area.html')

@app.route('/crear_jornada')
def crear_jornada():
    return render_template('crear_jornada.html')

@app.route('/listado_jornada')
def listado_jornada():
    return render_template('listado_jornada.html')

@app.route('/cerra_seccion')
def cerrar_seccion():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
