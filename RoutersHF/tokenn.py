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
            problema = fila['Problema']
            solucion = fila['Solucion']
            if problema in diccionario:
                diccionario[problema].append(solucion)
            else:
                diccionario[problema] = [solucion]
    return diccionario

diccionario = cargar_diccionario()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        soluciones = diccionario.get(descripcion, ["No se encontró solución para el problema."])
        
        resultado = f"<h5>Descripcion</h5> <li>{descripcion}</li> <h5>Solucion</h5> <ul>"
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