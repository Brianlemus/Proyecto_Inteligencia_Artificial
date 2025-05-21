import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def leer_direcciones():
    direcciones = []
    ruta_csv = os.path.join(DATA_DIR, 'direcciones.csv')
    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            texto = f"{fila['direccion']} #{fila['numero']}{fila['letra']} - {fila['nombre_casa']} ({fila['telefono']})"
            direcciones.append({'id': fila['id'], 'texto': texto})
    return direcciones

def leer_tipos_puesto():
    tipos = []
    ruta_csv = os.path.join(DATA_DIR, 'puesto.csv')    
    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            tipos.append({'id': fila['id'], 'nombre': fila['nombre']})    
    return tipos    

def leer_jornadas():
    jornadas = []
    ruta_csv = os.path.join(DATA_DIR, 'jornada.csv')
    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            jornadas.append({
                'id': fila['id'],
                'nombre_jornada': fila['nombre_jornada'],
                'hora_inicio': fila['hora_inicio'],
                'hora_fin': fila['hora_fin']
            })
    return jornadas

def leer_areas():
    areas = []
    ruta_csv = os.path.join(DATA_DIR, 'area.csv')
    try:
        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                areas.append({'id': fila['id'], 'nombre': fila['nombre']})
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {ruta_csv}")
    return areas

def guardar_csv(ruta_csv, campos, datos):
    file_exists = os.path.isfile(ruta_csv)
    with open(ruta_csv, 'a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        if not file_exists:
            escritor.writeheader()
        escritor.writerow(datos)
        
def leer_csv_como_dict(ruta):
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def leer_trabajadores():
    return leer_csv_como_dict(os.path.join(DATA_DIR, 'trabajadores.csv'))

def leer_residentes():
    return leer_csv_como_dict(os.path.join(DATA_DIR, 'residentes.csv'))

def leer_usuarios():
    return leer_csv_como_dict(os.path.join(DATA_DIR, 'usuarios.csv'))

def existe_dpi_o_correo(csv_path, dpi, correo):
    with open(csv_path, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['dpi'] == dpi or fila['correo'].lower() == correo.lower():
                return True
    return False

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # omitir la cabecera
        return list(reader)