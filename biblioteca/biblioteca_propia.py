import pandas as pd
import json
import os
import glob

#La ruta de la carpeta donde estan los JSON
ruta = 'Lugares/'

#funcion que permite almacenar los datos en una lista
def datos_restaurantes(ruta):
    restaurantes = []
    # un bucle que va a ir generando la ruta de cada una de las carpetas dentro de Lugares, las cuales son los municipios
    for lugar in os.listdir(ruta):
        #crear la variable que crea la ruta del lugar
        ubicacion_municipio = os.path.join(ruta,lugar)
        #verificar que los elementos de la carpeta Lugares son carpetas con isdir
        if os.path.isdir(ubicacion_municipio):
            #si es una carpeta entonces procede
            #ahora tengo que recorrer cada archivo dentro de cada ubicacion_municipio
            for archivo in os.listdir(ubicacion_municipio):
                #Tengo que abrir en modo lectura cada archivo que este dado por la ruta que se designa como ruta_archivo
                with open(os.path.join(ubicacion_municipio, archivo), 'r', encoding='utf-8') as ruta_archivo:
                    #agregar cada restaurante a la lista de restaurantes
                    restaurantes.append(json.load(ruta_archivo))
    return restaurantes

#funcion que cree el DataFrame de la lista
def df_datos(array):
    array_df = pd.DataFrame(array)
    return array_df

def datos_restaurante_municipio(lugar):
    ruta = f"Lugar/{lugar}"
    restaurantes = []
    for archivo in os.listdir(ruta):
        if archivo.endswith('.json'):
            with open(os.path.join(ruta, archivo), 'r', encoding='UTF-8') as f:
                restaurante = json.load(f)
                restaurantes.append(restaurante)
    return restaurantes

def salarios_cuba(ruta):
    salarios = None
    for archivo in os.listdir(ruta):
        if archivo == "salarios_cuba.json":
            with open(os.path.join(ruta, archivo), 'r') as f:
                salarios = json.load(f)
            break 
    return salarios

def precio_comida()




def horas(salario, precio_comida):