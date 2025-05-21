from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, template_folder='../templates')  # Ajusta la ruta si es necesario

def generar_grafica_pie_area():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(conteo_areas, labels=conteo_areas.index, autopct='%1.1f%%', startangle=140)
    plt.title('Porcentajes en Areas')
    plt.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_pie_prioridad():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_prioridad = df['prioridad'].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(conteo_prioridad, labels=conteo_prioridad.index, autopct='%1.1f%%', startangle=140)
    plt.title('Porcentaje de Prioridad')
    plt.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_barras_area():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightpink']
    conteo_areas.plot(kind='bar', color=colores[:len(conteo_areas)])
    plt.title('Total de tickets por Area')
    plt.xlabel('Area')
    plt.ylabel('Numero de Tickets')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_barras_prioridad():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_prioridad = df['prioridad'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightpink']
    conteo_prioridad.plot(kind='bar', color=colores[:len(conteo_prioridad)])
    plt.title('Total de tickets por prioridad')
    plt.xlabel('Prioridad')
    plt.ylabel('Número de Tickets')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

@app.route('/')
def index():
    return redirect(url_for('mostrar_grafica_pie_area'))

@app.route('/pie_area')
def mostrar_grafica_pie_area():
    imagen = generar_grafica_pie_area()
    if imagen:
        return render_template('pie_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@app.route('/pie_prioridad')
def mostrar_grafica_pie_prioridad():
    imagen = generar_grafica_pie_prioridad()
    if imagen:
        return render_template('pie_prioridad.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@app.route('/barras_area')
def mostrar_grafica_barras_area():
    imagen = generar_grafica_barras_area()
    if imagen:
        return render_template('barras_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@app.route('/barras_prioridad')
def mostrar_grafica_barras_prioridad():
    imagen = generar_grafica_barras_prioridad()
    if imagen:
        return render_template('barras_prioridad.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

if __name__ == '__main__':
    app.run(debug=True)