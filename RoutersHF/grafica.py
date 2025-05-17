from flask import Flask, render_template,redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, template_folder='../templates')  # Ajusta la ruta si es necesario

def generar_grafica_pie():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.pie(conteo_areas, labels=conteo_areas.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribución de Tickets por Área')
    plt.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

def generar_grafica_barras():
    try:
        df = pd.read_csv('ticket.csv', header=None, names=['id', 'fecha', 'prioridad', 'area', 'problema', 'estado'])
    except FileNotFoundError:
        return None
    
    conteo_areas = df['area'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colores = ['skyblue', 'lightgreen', 'salmon', 'gold', 'lightcoral', 'lightpink']  # Colores personalizados
    conteo_areas.plot(kind='bar', color=colores[:len(conteo_areas)])  # Ajustar colores según el número de áreas
    plt.title('Frecuencia de Tickets por Área')
    plt.xlabel('Área')
    plt.ylabel('Número de Tickets')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return imagen

#cambio de route

@app.route('/')
def index():
    return redirect(url_for('mostrar_grafica_barras'))

@app.route('/pie_area')
def mostrar_grafica_pie():
    imagen = generar_grafica_pie()
    if imagen:
        return render_template('pie_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

@app.route('/barras_area')
def mostrar_grafica_barras():
    imagen = generar_grafica_barras()
    if imagen:
        return render_template('barras_area.html', imagen=imagen)
    else:
        return "No se pudo leer el archivo CSV o no hay datos para mostrar."

if __name__ == '__main__':
    app.run(debug=True)
