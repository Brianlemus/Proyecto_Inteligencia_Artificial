from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__, template_folder='../templates')
DICCIONARIO_CSV = 'diccionario.csv'

@app.route('/')
def index():
    return render_template('crearticket.html')

@app.route('/solucion')
def solucion():
    return render_template('solucion.html')

@app.route('/seguimiento_ticket')
def seguimiento_ticket():
    return render_template('seguimiento.html')

if __name__ == '__main__':
    app.run(debug=True)