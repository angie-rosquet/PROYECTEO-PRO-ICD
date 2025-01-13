import pandas as pd
import json
import os
import glob
#La ruta de la carpeta donde estan mis JSON
ruta = 'Lugares/'
#Lista vacia donde se va a ir almacenando la info de cada restaurante
restaurantes_datos = []
#Crear una lista que contenga el nombre de cada una de las carpetas dentro de lugares, que se corresponde con los 15 Municipios
municipios = os.listdir(ruta)
for municipio in municipios :
    ruta_municipio = os.path.join(ruta, municipio)
    if os.path.isdir(ruta_municipio):
        archivos_json = glob.glob(os.path.join(ruta_municipio, '*.json'))
        for archivo in archivos_json:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
                datos_json['municipio'] = municipio
                restaurantes_datos.append(datos_json)


df_restaurantes = pd.DataFrame(restaurantes_datos)
print(df_restaurantes)