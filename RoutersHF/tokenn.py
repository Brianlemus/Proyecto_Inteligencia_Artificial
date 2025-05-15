from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__, template_folder='../templates')

# Función para cargar problemas y soluciones desde el archivo CSV
def cargar_diccionario():
    diccionario = {}
    with open('diccionario.csv', mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            area = fila['Area']
            problema = fila['Problema']
            solucion = fila['Solucion']
            if problema not in diccionario:
                diccionario[problema] = {'soluciones': [], 'area': area}
            diccionario[problema]['soluciones'].append(solucion)
    return diccionario

diccionario = cargar_diccionario()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        # Obtener el problema y sus datos
        data = diccionario.get(descripcion, None)
        
        if data:
            area = data['area']
            soluciones = data['soluciones']
        else:
            area = "Area desconocida"
            soluciones = ["No se encontró solución para el problema."]
        
        resultado = f"<h5>Área</h5><li>{area}</li><h5>Descripción</h5><li>{descripcion}</li><h5>Solución</h5><ul>"
        for solucion in soluciones:
            resultado += f"<li>{solucion}</li>"
        resultado += "</ul>"
        
        return redirect(url_for('mostrar_respuesta', resultado=resultado))

    return render_template('crearticket.html')

@app.route('/mostrar_respuesta')
def mostrar_respuesta():
    resultado = request.args.get('resultado', '')
    return render_template('solucion.html', resultado=resultado)

@app.route('/seguimiento_ticket')
def seguimiento_ticket():
    return render_template('seguimiento.html')

if __name__ == '__main__':
    app.run(debug=True)